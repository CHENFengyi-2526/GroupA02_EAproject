from tables.users import create_table_users
from tables.elderly_profiles import create_table_elderly_profiles
from tables.family_contacts import create_table_family_contacts
from tables.user_devices import create_table_user_devices
from tables.consent_records import create_table_consent_records
from tables.family_elderly_links import create_table_family_elderly_links
from tables.access_logs import create_table_access_logs
from tables.user_settings import create_table_user_settings

if __name__ == "__main__":
    print("===== Start creating all 8 tables =====")
    create_table_users()
    create_table_elderly_profiles()
    create_table_family_contacts()
    create_table_user_devices()
    create_table_consent_records()
    create_table_family_elderly_links()
    create_table_access_logs()
    create_table_user_settings()
    print("\n===== All tables created successfully =====")
