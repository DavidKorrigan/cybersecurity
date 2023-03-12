# Basic Windows PowerShell Commands

- Retrieve all the cmdlets installed on the host.

`Get-Command`
```
CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           Add-AppPackage                                     2.0.1.0    Appx
Alias           Add-AppPackageVolume                               2.0.1.0    Appx
Alias           Add-AppProvisionedPackage                          3.0        Dism
Alias           Add-ProvisionedAppPackage                          3.0        Dism
Alias           Add-ProvisionedAppSharedPackageContainer           3.0        Dism
[...]
```

- Filtering on the beginning of the command name to find.

`Get-Command Get-Local*`
```
CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Cmdlet          Get-LocalGroup                                     1.0.0.0    Microsoft.PowerShell.LocalAccounts
Cmdlet          Get-LocalGroupMember                               1.0.0.0    Microsoft.PowerShell.LocalAccounts
Cmdlet          Get-LocalUser                                      1.0.0.0    Microsoft.PowerShell.LocalAccounts
```

- Filtering on the end of the command name to find.

`Get-Command *User`
```
CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Cmdlet          Disable-LocalUser                                  1.0.0.0    Microsoft.PowerShell.LocalAccounts
Cmdlet          Enable-LocalUser                                   1.0.0.0    Microsoft.PowerShell.LocalAccounts
Cmdlet          Get-LocalUser                                      1.0.0.0    Microsoft.PowerShell.LocalAccounts
Cmdlet          New-LocalUser                                      1.0.0.0    Microsoft.PowerShell.LocalAccounts
Cmdlet          Remove-LocalUser                                   1.0.0.0    Microsoft.PowerShell.LocalAccounts
Cmdlet          Rename-LocalUser                                   1.0.0.0    Microsoft.PowerShell.LocalAccounts
Cmdlet          Set-LocalUser                                      1.0.0.0    Microsoft.PowerShell.LocalAccounts
```

- Get help on a command help.

`Get-Help Get-LocalUser`
```
NAME
    Get-LocalUser

SYNTAX
    Get-LocalUser [[-Name] <string[]>]  [<CommonParameters>]

    Get-LocalUser [[-SID] <SecurityIdentifier[]>]  [<CommonParameters>]


ALIASES
    glu
```

- Search recursively for file and ignore errors.

`Get-ChildItem -Path C:\ -Include *password.txt* -File -Recurse -ErrorAction SilentlyContinue`

```
    Directory: C:\GIT


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        12/03/2023     14:00              0 my_password.txt
```

- Search for file containing string.

`Get-ChildItem C:\* -Recurse -ErrorAction SilentlyContinue | Select-String -pattern password`
```
C:\GIT\my_password.txt:1:password 1234
```

- Display file content.

`Get-Content "C:\GIT\my_password.txt"`
```
password 1234
```

- Count number of items returned with | measure.

`Get-Command Get-Local* | measure`
```
Count    : 3
Average  :
Sum      :
Maximum  :
Minimum  :
Property :
```

- Display current location.

`Get-Location`
```
Path
----
C:\GIT
```

- Compute the hash of a file.

`Get-FileHash -Path "C:\GIT\my_password.txt" -Algorithm SHA256`
```
Algorithm       Hash                                                                   Path
---------       ----                                                                   ----
SHA256          B1A87F320DBDEDCFBCDC35976518A42E60530DD4656398C86945E4954AB71E32       C:\GIT\my_password.txt
```

- Encode file in base64.

certutil -encode "C:\GIT\my_password.txt" my_password.b64
```
Input Length = 13
Output Length = 78
CertUtil: -encode command completed successfully.
```

- Decode file from base64.
`certutil -decode "C:\GIT\my_password.b64" my_password.txt2`
```
Input Length = 78
Output Length = 13
CertUtil: -decode command completed successfully.
```

- Display owner of an object

`Get-Acl C:/GIT`
```
    Directory: C:\

Path Owner               Access
---- -----               ------
GIT  LAPTOP\bob BUILTIN\Administrators Allow  FullControl...
```

## Enumeration
- Display all the methods & properties of cmdlets with -MemberType
`Get-LocalGroup | Get-Member`
```
   TypeName: Microsoft.PowerShell.Commands.LocalGroup

Name            MemberType Definition
----            ---------- ----------
Clone           Method     Microsoft.PowerShell.Commands.LocalGroup Clone()
Equals          Method     bool Equals(System.Object obj)
GetHashCode     Method     int GetHashCode()
GetType         Method     type GetType()
ToString        Method     string ToString()
Description     Property   string Description {get;set;}
Name            Property   string Name {get;set;}
ObjectClass     Property   string ObjectClass {get;set;}
PrincipalSource Property   System.Nullable[Microsoft.PowerShell.Commands.PrincipalSource] PrincipalSource {get;set;}
SID             Property   System.Security.Principal.SecurityIdentifier SID {get;set;}
```

- Display Method of cmdlets

`Get-LocalGroup | Get-Member -MemberType Method`
```
   TypeName: Microsoft.PowerShell.Commands.LocalGroup

Name        MemberType Definition
----        ---------- ----------
Clone       Method     Microsoft.PowerShell.Commands.LocalGroup Clone()
Equals      Method     bool Equals(System.Object obj)
GetHashCode Method     int GetHashCode()
GetType     Method     type GetType()
ToString    Method     string ToString()
```

- Display Property of cmdlets

`Get-LocalGroup | Get-Member -MemberType Property`
```
   TypeName: Microsoft.PowerShell.Commands.LocalGroup

Name            MemberType Definition
----            ---------- ----------
Description     Property   string Description {get;set;}
Name            Property   string Name {get;set;}
ObjectClass     Property   string ObjectClass {get;set;}
PrincipalSource Property   System.Nullable[Microsoft.PowerShell.Commands.PrincipalSource] PrincipalSource {get;set;}
SID             Property   System.Security.Principal.SecurityIdentifier SID {get;set;}
```

- Retrieve All Local Users

`Get-LocalUser`
```
Name               Enabled Description
----               ------- -----------
Administrator      False   Built-in account for administering the computer/domain
bob                True
DefaultAccount     False   A user account managed by the system.
Guest              False   Built-in account for guest access to the computer/domain
```

- Retrieve Local User based on name

`Get-LocalUser -Name bob`
```
Name   Enabled Description
----   ------- -----------
bob    True
```

- Retrieve Local User based on SID

`Get-LocalUser -SID "S-1-5[...]5-501"`
```
Name   Enabled Description
----   ------- -----------
bob    True
```

- Retrieve Local User based on a property value

`Get-LocalUser | Where-Object -Property PasswordRequired -Match false`
```
Name   Enabled Description
----   ------- -----------
bob    True
```

- Retrieve all the local groups

`Get-LocalGroup`
```
Name                          Description
----                          -----------
Administrators                Administrators have complete and unrestricted access to the computer/domain
Device Owners                 Members of this group can change system-wide settings.
Distributed COM Users         Members are allowed to launch, activate and use Distributed COM objects on this machine.
Event Log Readers             Members of this group can read event logs from local machine
Guests                        Guests have the same access as members of the Users group by default, except for the G...
Hyper-V Administrators        Members of this group have complete and unrestricted access to all features of Hyper-V.
IIS_IUSRS                     Built-in group used by Internet Information Services.
Performance Log Users         Members of this group may schedule logging of performance counters, enable trace provi...
Performance Monitor Users     Members of this group can access performance counter data locally and remotely
Remote Management Users       Members of this group can access WMI resources over management protocols (such as WS-M...
System Managed Accounts Group Members of this group are managed by the system.
Users                         Users are prevented from making accidental or intentional system-wide changes and can ...
```

## Network
- Download file

`Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DavidKorrigan/cybersecurity/main/README.md" -OutFile "readme.md"`

- GET IP address info

`Get-NetIPAddress`
```
[...]
IPAddress         : 127.0.0.1
InterfaceIndex    : 1
InterfaceAlias    : Loopback Pseudo-Interface 1
AddressFamily     : IPv4
Type              : Unicast
PrefixLength      : 8
PrefixOrigin      : WellKnown
SuffixOrigin      : WellKnown
AddressState      : Preferred
ValidLifetime     :
PreferredLifetime :
SkipAsSource      : False
PolicyStore       : ActiveStore
[...]
```

- Get listening ports

`Get-NetTCPConnection | Where-Object -Property State -Match Listen`
```
LocalAddress                        LocalPort RemoteAddress                       RemotePort State       AppliedSetting
------------                        --------- -------------                       ---------- -----       --------------
::                                  49676     ::                                  0          Listen
[...]
```

## System

- Display all the patches installed.

`Get-Hotfix`
```
Source        Description      HotFixID      InstalledBy          InstalledOn
------        -----------      --------      -----------          -----------
LAPTOP        Update           KB5022497     NT AUTHORITY\SYSTEM  18/02/2023 00:00:00
[...]
```

- Display a specific patch based on its ID.

`Get-Hotfix -Id KB4023834`
```
Source        Description      HotFixID      InstalledBy          InstalledOn
------        -----------      --------      -----------          -----------
FAMILY-LAPTOP Update           KB5022497     NT AUTHORITY\SYSTEM  18/02/2023 00:00:00
```


- Display process all processes.

`Get-Process`
```
Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName
-------  ------    -----      -----     ------     --  -- -----------
    162      10     2832       6920              5180   0 AggregatorHost
[...]
```

- Display a specific task based on its name.

`Get-ScheduledTask -TaskName SpaceAgentTask`
```
TaskPath                                       TaskName                          State
--------                                       --------                          -----
\Microsoft\Windows\SpacePort\                  SpaceAgentTask                    Ready
```

