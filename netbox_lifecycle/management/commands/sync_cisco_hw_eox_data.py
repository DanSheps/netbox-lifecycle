import requests
import json
import django.utils.text

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

from dcim.models import DeviceType, ModuleType, Manufacturer
from netbox_lifecycle.models import hardware


class Command(BaseCommand):
    help = 'Sync Hardware Lifecycle Information from Cisco EoX Support API'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--manufacturer',
            action='store_true',
            default='Cisco',
            help='Manufacturer name (default: Cisco)',
        )

    def api_logon(self):
        PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("netbox_lifecycle", dict())
        CISCO_CLIENT_ID = PLUGIN_SETTINGS.get("cisco_support_api_client_id", "")
        CISCO_CLIENT_SECRET = PLUGIN_SETTINGS.get("cisco_support_api_client_secret", "")

        token_url = "https://id.cisco.com/oauth2/default/v1/token"
        data = {'grant_type': 'client_credentials', 'client_id': CISCO_CLIENT_ID, 'client_secret': CISCO_CLIENT_SECRET}

        access_token_response = requests.post(token_url, data=data)

        tokens = json.loads(access_token_response.text)

        api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token'], 'Accept': 'application/json'}

        return api_call_headers

    def update_lifecycle_data(self, pid, hardware_type, eox_data):

        hw_obj = DeviceType()
        content_type = ContentType()

        match hardware_type:
            case "devicetype":
                content_type = ContentType.objects.get(app_label="dcim", model="devicetype")
                try:
                    # Get the device type object for the supplied PID
                    hw_obj = DeviceType.objects.get(part_number=pid)
                except MultipleObjectsReturned:
                    # Error if Netbox returns multiple duplicate PN's
                    self.stdout.write(self.style.NOTICE(f"ERROR: Multiple objects exist with Part Number {pid}"))
                    return

            case "moduletype":
                content_type = ContentType.objects.get(app_label="dcim", model="moduletype")
                try:
                    # Get the device type object for the supplied PID
                    hw_obj = ModuleType.objects.get(part_number=pid)
                except MultipleObjectsReturned:
                    # Error if Netbox returns multiple duplicate PN's
                    self.stdout.write(self.style.NOTICE(f"ERROR: Multiple objects exist with Part Number {pid}"))
                    return

            case _:
                raise CommandError('Invalid hardware_type argument defined.')
                exit

        # Check if a HardwareLifecycle record already exists
        try:
            hw_lifecycle = hardware.HardwareLifecycle.objects.get(assigned_object_id=hw_obj.id, assigned_object_type_id=content_type.id)
            self.stdout.write(self.style.SUCCESS(f"{pid} - has an existing NetBox hardware lifecycle record"))
        # If not, create a new one for this Device Type
        except hardware.HardwareLifecycle.DoesNotExist:
            hw_lifecycle = hardware.HardwareLifecycle(assigned_object_id=hw_obj.id, assigned_object_type_id=content_type.id)
            self.stdout.write(self.style.NOTICE(f"{pid} - has no existing NetBox hardware lifecycle record"))

        # Only save if something has changed
        value_changed = False
        # Sale and Support End-of values both required for a lifecycle record
        end_of_sale_defined = False
        end_of_support_defined = False

        try:
            # Check if JSON contains EndOfSaleDate with a value defined
            if not eox_data["EOXRecord"][0]["EndOfSaleDate"]["value"]:
                self.stdout.write(self.style.NOTICE(f"{pid} - has no end_of_sale_date"))
            else:
                end_of_sale_date_string = eox_data["EOXRecord"][0]["EndOfSaleDate"]["value"]
                # Cast this value to datetime.date object
                end_of_sale_date = datetime.strptime(end_of_sale_date_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS(f"{pid} - end_of_sale_date: {end_of_sale_date}"))
                # Check if our HardwareLifecycle object has a different date to that returned from api
                if hw_lifecycle.end_of_sale != end_of_sale_date:
                    hw_lifecycle.end_of_sale = end_of_sale_date
                    end_of_sale_defined = True
                    value_changed = True

        # Do nothing when JSON field does not exist
        except KeyError:
            self.stdout.write(self.style.NOTICE(f"{pid} - has no end_of_sale_date"))

        try:
            if not eox_data["EOXRecord"][0]["EndOfSWMaintenanceReleases"]["value"]:
                self.stdout.write(self.style.NOTICE(f"{pid} - has no end_of_sw_maintenance_releases"))
            else:
                end_of_maintenance_string = eox_data["EOXRecord"][0]["EndOfSWMaintenanceReleases"]["value"]
                end_of_maintenance = datetime.strptime(end_of_maintenance_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS(f"{pid} - end_of_sw_maintenance_releases: {end_of_maintenance}"))

                if hw_lifecycle.end_of_maintenance != end_of_maintenance:
                    hw_lifecycle.end_of_maintenance = end_of_maintenance
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE(f"{pid} - has no end_of_sw_maintenance_releases"))

        try:
            if not eox_data["EOXRecord"][0]["EndOfSecurityVulSupportDate"]["value"]:
                self.stdout.write(self.style.NOTICE(f"{pid} - has no end_of_security_vul_support_date"))
            else:
                end_of_security_string = eox_data["EOXRecord"][0]["EndOfSecurityVulSupportDate"]["value"]
                end_of_security_date = datetime.strptime(end_of_security_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS(f"{pid} - end_of_security_vul_support_date: {end_of_security_date}"))

                if hw_lifecycle.end_of_security != end_of_security_date:
                    hw_lifecycle.end_of_security = end_of_security_date
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE(f"{pid} - has no end_of_security_vul_support_date"))

        try:
            if not eox_data["EOXRecord"][0]["EndOfSvcAttachDate"]["value"]:
                self.stdout.write(self.style.NOTICE(f"{pid} - has no end_of_service_attach_date"))
            else:
                last_contract_date_string = eox_data["EOXRecord"][0]["EndOfSvcAttachDate"]["value"]
                last_contract_date_date = datetime.strptime(last_contract_date_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS(f"{pid} - end_of_service_attach_date: {last_contract_date_date}"))

                if hw_lifecycle.last_contract_date != last_contract_date_date:
                    hw_lifecycle.last_contract_date = last_contract_date_date
                    value_changed = True
        except KeyError:
            self.stdout.write(self.style.NOTICE(f"{pid} - has no end_of_service_attach_date"))

        try:
            if not eox_data["EOXRecord"][0]["LastDateOfSupport"]["value"]:
                self.stdout.write(self.style.NOTICE(f"{pid} - has no last_date_of_support"))
            else:
                end_of_support_string = eox_data["EOXRecord"][0]["LastDateOfSupport"]["value"]
                end_of_support_date = datetime.strptime(end_of_support_string, '%Y-%m-%d').date()
                self.stdout.write(self.style.SUCCESS(f"{pid} - last_date_of_support: {end_of_support_date}"))

                if hw_lifecycle.end_of_support != end_of_support_date:
                    hw_lifecycle.end_of_support = end_of_support_date
                    value_changed = True
                    end_of_support_defined = True
        except KeyError:
            self.stdout.write(self.style.NOTICE(f"{pid} - has no last_date_of_support"))

        if (value_changed and end_of_sale_defined and end_of_support_defined):
            hw_lifecycle.save()

        return

    def get_product_ids(self, manufacturer):
        results = {}

        # Query for the Manufacturer First
        try:
            manufacturer_results = Manufacturer.objects.get(name=manufacturer)
        except Manufacturer.DoesNotExist:
            raise CommandError(f'Manufacturer "{manufacturer}" does not exist')

        self.stdout.write(self.style.SUCCESS(f'Found manufacturer "{manufacturer_results}"'))

        # trying to get all device types and base PIDs associated with this manufacturer
        try:
            devicetype_results = DeviceType.objects.filter(manufacturer=manufacturer_results)
            for devicetype in devicetype_results:
                if not devicetype.part_number:
                    self.stdout.write(self.style.WARNING(f'Found device type "{devicetype}" WITHOUT Part Number - SKIPPING'))
                    continue

                self.stdout.write(self.style.SUCCESS(f'Found device type "{devicetype}" with Part Number "{devicetype.part_number}"'))
                results[devicetype.part_number] = 'devicetype'

        except DeviceType.DoesNotExist:
            raise CommandError(f'Manufacturer "{manufacturer_results}" has no Device Types')

        # trying to get all module types and base PIDs associated with this manufacturer
        try:
            moduletype_results = ModuleType.objects.filter(manufacturer=manufacturer_results)
            for moduletype in moduletype_results:
                if not moduletype.part_number:
                    self.stdout.write(self.style.WARNING(f'Found device type "{moduletype}" WITHOUT Part Number - SKIPPING'))
                    continue

                self.stdout.write(self.style.SUCCESS(f'Found device type "{moduletype}" with Part Number "{moduletype.part_number}"'))
                results[moduletype.part_number] = 'moduletype'
        except DeviceType.DoesNotExist:
            raise CommandError(f'Manufacturer "{manufacturer_results}" has no Module Types')

        return results

    # Main entry point for the sync_cisco_hw_eox_data command of manage.py
    def handle(self, *args, **kwargs):
        MANUFACTURER = "Cisco"

        # Logon one time and gather the required API key
        api_call_headers = self.api_logon()

        # Step 1: Get all PIDs for all Device Types of that particular manufacturer
        product_ids = self.get_product_ids(MANUFACTURER)
        self.stdout.write(self.style.SUCCESS(f'Querying API for these PIDs: ' + ', '.join(product_ids)))

        for pid, hw_type in product_ids.items():
            url = f'https://apix.cisco.com/supporttools/eox/rest/5/EOXByProductID/1/{pid}?responseencoding=json'
            api_call_response = requests.get(url, headers=api_call_headers)
            self.stdout.write(self.style.SUCCESS('Call ' + url))

            # sanatize file name
            filename = django.utils.text.get_valid_filename(f'{pid}.json')

            # debug API answer to text file
            # with open('/opt/netbox_Lifecycle_cisco_xapi_results/%s' % filename, 'w') as outfile:
            #    outfile.write(api_call_response.text)

            # Validate response from Cisco
            if api_call_response.status_code == 200:

                # Deserialize JSON API Response into Python object "data"
                data = json.loads(api_call_response.text)

                # Call our Device Type Update method for that particular PID
                self.update_lifecycle_data(pid, hw_type, data)

            else:

                # Show an error
                self.stdout.write(self.style.ERROR('API Error: ' + api_call_response.text))
