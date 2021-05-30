import influxdb_client

from machine.management.commands import populator


class Command(populator.Populator):
    fixture_path = './resources/task/machines.csv'

    def parse_row(self, row):
        return (influxdb_client.Point('machines')
                .tag('key', row['key'])
                .field('name', row['name'])
                .time(0)
                .to_line_protocol())  # yapf: disable
