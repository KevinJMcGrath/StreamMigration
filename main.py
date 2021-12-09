import package_logger

from sfdc import migration

package_logger.initialize_logging()

def run_main():
    # migration.test_contact_insert()

    migration.migrate_stream_users(limit=200, only_client_users=True)

if __name__ == '__main__':
    run_main()