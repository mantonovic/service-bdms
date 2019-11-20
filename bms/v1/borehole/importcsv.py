# -*- coding: utf-8 -*-
import csv
from bms.v1.action import Action

from bms.v1.borehole.create import CreateBorehole
from bms.v1.borehole.patch import PatchBorehole
from bms.v1.borehole.check import CheckBorehole

"""

The CSV file shall have this structure, without the header:

location_east;location_north;original_name
2679500;1177500;prova1
2669940;1209820;prova2


"""

class ImportCsv(Action):

    async def execute(self, file, id, user):

        check = CheckBorehole(self.conn)
        reader = csv.reader(file, delimiter=';', quotechar='"')
        rows = list(reader)
        line = 1
        for row in rows[1:]:
            line += 1
            if len(row) != 3:
                raise Exception("Columns number wrong")

            location_x = float(row[0])
            location_y = float(row[1])
            if (
                location_x < 2485869.5728 or
                location_x > 2837076.5648
            ) or (
                location_y < 1076443.1884 or
                location_y > 1299941.7864
            ):
                raise Exception(f"Line {line}: coordinates outside Switzerland")

            data = await check.execute(
                'extended.original_name', row[2]
            )

            if data['check'] is False:
                raise Exception(f'Line {line}: Borehole "{row[2]}" already exists')

        create = CreateBorehole(self.conn)
        patch = PatchBorehole(self.conn)

        for row in rows[1:]:

            location_x = float(row[0])
            location_y = float(row[1])

            # Creating a new borehole
            bid = await create.execute(id, user)

            # Setting the coordinates
            await patch.execute(
                bid['id'],
                'location_x',
                location_x,
                user
            )

            await patch.execute(
                bid['id'],
                'location_y',
                location_y,
                user
            )

            await patch.execute(
                bid['id'],
                'extended.original_name',
                row[2],
                user
            )

        return None
