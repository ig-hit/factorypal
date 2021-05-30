import influxdb_client

from machine.management.commands import populator


class Command(populator.Populator):
    fixture_path = './resources/task/parameters.csv'

    def parse_row(self, row):
        return (influxdb_client.Point('params')
                .tag('machine_key', row['machine_key'])
                .field(row['key'], row['value'])
                .to_line_protocol())  # yapf: disable
