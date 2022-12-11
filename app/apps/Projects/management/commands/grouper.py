import pandas as pd
from datetime import timedelta

from django.core.management.base import BaseCommand

from apps.Projects.models import (
    SourceDataRowRaw,
    SourceDataSchemaMapping,
    GroupedSourceData,
    DataSource,
    AggregationControl,
)
from time import sleep


def row_is_indexable(series):
    # Make Sure: do not group by rows which should not be grouped
    return series.shape[0] > 4 * series.unique().shape[0]


def get_aggregation_methods_for_row(series):
    methods = ["count"]
    if series.dtype == "int" or series.dtype == "float":
        methods += ["mean", "sum"]
    return methods


def group_count(df_root, group_by_freq: str, feature_name: str):
    return df_root\
        .groupby([pd.Grouper(freq=group_by_freq, dropna=False), df_root[feature_name]])\
        .size()\
        .reset_index(name='count')


def group_number(df_root, group_by_freq: str, feature_name: str, aggr_method: str):
    tmp = df_root\
      .groupby([pd.Grouper(freq=group_by_freq, dropna=False), df_root[feature_name]])\
      .agg(aggr_method) \
      .reset_index()
    tmp.rename(columns={col: f"{aggr_method}_{col}" for col in tmp.columns}, inplace=True)
    return tmp


def update_or_create_group_counts(row, source, column_name, method):
    try:
        entity = GroupedSourceData.objects.get(
            source=source,
            timestamp=row["timestamp"],
            type="g1",
            by_key=column_name,
            method=method,
        )
        entity.values = {"count": row["count"]}
        entity.save()
    except GroupedSourceData.DoesNotExist:
        GroupedSourceData.objects.create(
            source=source,
            timestamp=row["timestamp"],
            type="g1",
            by_key=column_name,
            method=method,
            values=row["count"]
        )


def update_or_create_group_numbers(row, source, column_name, method, df):
    values = {
        f"{method}_{column_name}": row[f"{method}_{column_name}"]
        for col_name in df.columns if column_name != "timestamp" and col_name != column_name
    }
    try:
        entity = GroupedSourceData.objects.get(
            source=source,
            timestamp=row["timestamp"],
            type="g1",
            by_key=column_name,
            method=method,
        )
        entity.values = values
        entity.save()
    except GroupedSourceData.DoesNotExist:
        GroupedSourceData.objects.create(
            source=source,
            timestamp=row["timestamp"],
            type="g1",
            by_key=column_name,
            method=method,
            values=values
        )



class Command(BaseCommand):

    def load_dataframe(self, source_id: int):
        data = GroupedSourceData.objects.filter(source__id=source_id).order_by("timestamp")
        query_args = {
            "source__id": source_id
        }
        if data.exists():
            last_run = data.last()
            # 24 hours before last run dt for being able to check some aggregation rules
            min_dt = last_run.timestamp - timedelta(hours=24)
            query_args["timestamp__gte"] = min_dt
        columns = [f"key_{i}" for i in range(len(SourceDataSchemaMapping.objects.get(source__id=source_id).mapping.values()))]
        data = SourceDataRowRaw.objects.filter(**query_args)
        entities = [
            [entity.timestamp] + list(entity.value.values())
            for entity in data.all()
        ]
        df = pd.DataFrame(entities, columns=["timestamp"] + list(columns))
        df.set_index("timestamp", inplace=True)
        return df

    def perform_group_count(self, df, column_name, source):
        count_df = group_count(df, "H", column_name)
        count_df.apply(
            lambda row: update_or_create_group_counts(row, source, column_name, "count"),
            axis=1
        )

    def perform_group_number(self, df, column_name, aggr_method, source):
        aggr_df = group_number(df, "H", column_name, aggr_method=aggr_method)
        aggr_df.apply(
            lambda row: update_or_create_group_numbers(row, source, column_name, aggr_method, df),
            axis=1
        )

    def perform_grouping(self, df, source):
        for col in df.columns:
            if not row_is_indexable(df[col]):
                continue
            methods = get_aggregation_methods_for_row(df[col])
            self.stdout.write(f"Start Grouping for {source.id}")
            self.perform_group_count(df, col, source)
            if "mean" in methods and "sum" in methods:
                self.stdout.write(f"Start Sum for {source.id}")
                self.perform_group_number(df, col, "sum", source)
                self.stdout.write(f"Start Mean for {source.id}")
                self.perform_group_number(df, col, "mean", source)

    def reset_process(self, source):
        GroupedSourceData.objects.filter(source=source).delete()

    def handle(self, *args, **options):
        unique_source_ids = list(set(SourceDataRowRaw.objects.values_list("source", flat=True).distinct()))
        for source_id in unique_source_ids:
            self.stdout.write(f"Start Operation for {source_id}")
            try:
                source = DataSource.objects.get(id=source_id)
                control, _ = AggregationControl.objects.get_or_create(source=source)
                if control.reset_process:
                    self.reset_process(source)
                    control.reset_process = False
                    control.save()
                df = self.load_dataframe(source_id)
                self.perform_grouping(df, source)
            except Exception as e:
                self.stdout.write(f"Operation for {source_id} Failed: {e}")
        self.stdout.write("Start Sleeping for 2 Minutes")
        sleep(120)
