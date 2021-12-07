from sfdc import migration

def run_main():
    migration.migrate_stream_users(1)

if __name__ == '__main__':
    run_main()