# Patching SharePoint

## First Things

- Snapshot of all servers (Hypervisor)
- Backups of SQL Tables
- (Optional) Add `app_offline.htm` file at the root of each web application folder

## Steps

1. **Download CUs**
    - Best Resource: [https://blog.stefan-gossner.com/](https://blog.stefan-gossner.com/)
    - Patch n-1 frequency
    - There are always 2 files to install
        - If update runs from Windows update, it usually only installs just one of the files.

2. **Copy CU files**
    - Create folder in D: on each SharePoint 2019 server (APPS1, FEDC1, FEDC2, SRCH1)
        - Folder Title: `YearMonth-CU`
        - Copy both files into the new folder

3. **Log into Each Server as SharePoint Farm Admin**
    - Steps below should be executed as SharePoint Farm Admin

4. **Run EXEs**
    - **Run CU on APPS1 1st**
        - Install file starting with `sts` 1st - Run As `Admin`
        - Install file starting with `wssloc` - Run As `Admin`
    - Install of APPS1 needs to be successful before proceeding to other servers

5. **STOP services on SRCH1**
    - Not stopping these services will increase the time to install CUs
        - SharePoint Search Host Controller
        - SharePoint Server Search 16
        - SharePoint Timer Service

6. **Run CU install on all other servers**
    - Can be run at the same time
    - Starting with `sts` file and then `wssloc` - Run as Admin

7. **Start services on SRCH1**
    - SharePoint Search Host Controller
    - SharePoint Server Search 16
    - SharePoint Timer Service

8. **RUN SharePoint Configuration Wizard from APPS1**
    - Run as `Admin`
    - **Could Run from CMD**: `PSConfig.exe -cmd upgrade -inplace b2b -wait -Force`
    - If Configuration Wizard Successful:
        - Confirm in IIS:
            1. Each Web Application Pool is started
            2. Each Web site is started
            3. Services are running (SharePoint Services, WWW publishing Service, IIS Admin Service)
            4. Check Servers in Farm (`/_admin/FarmServers.aspx`) Status
        - Proceed to each server to run SharePoint Configuration Wizard:
            1. Only Run 1 Configuration Wizard at a time
            2. Run as Admin
            3. Confirm Wizard is successful
    - If Configuration Wizard Unsuccessful:
        - Clear config cache (Maybe just restart the server)
        - Resolve errors and re-run configuration wizard
        - Each time the wizard is run, it will create a log file. Link provided in failure message box.
        - Don't proceed on to other servers until APPS1 errors are resolved.
        - Running into issues.

9. **POST PATCHING CHECKS**
    - Confirm Infowise TimerJobs are still installed, if not run Repair. (If upgrading Infowise and TimerJobs not present, must run repair on current version before upgrading.)
    - Confirm Search is working
    - Delete extra snapshots from Hypervisor. (Leave only the most recent snapshot)

## Scripts

```shell
PSConfig.exe -cmd upgrade -inplace b2b -wait -cmd applicationcontent -install -cmd installfeatures -cmd secureresources -cmd services -install
```
