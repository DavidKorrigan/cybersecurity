<#
.SYNOPSIS
   Returns list of ports listening with associated services.
.DESCRIPTION
   Returns list of ports listening with associated services.
.EXAMPLE
   Get-ListeningPorts
#>

function Get-ListeningPorts {
    [CmdletBinding()]
    [Alias()]
    [OutputType("List of ports")]
    Param()

    Begin {
        Write-Verbose "Starting $($CurrentConnection.list)"

        # Get all the listening port on the host
        $connection = Get-NetTCPConnection -State Listen

        # Prepare & call HTTP request to retrieve port dictionary.
        $url = 'https://raw.githubusercontent.com/DavidKorrigan/cybersecurity/main/dictionaries/ports_and_services.json'
        $r = Invoke-WebRequest $url | ConvertFrom-Json | Select

        # Prepare output label
        $LocalPort = "Local Port"
        $ServiceName = "Service Name"
        $ServiceDescription = "Service Description"
    }

    Process {
        # For each port search in the disctionary.
        foreach($port in $connection.LocalPort){
            Try {
                $service = $r.$port
                if (!$service) {
                    $name = "Unknown"
                    $description = "Not a standard port"
                } else {
                    $interface = $port.LocalAddress
                    $name = $service.name
                    $description = $service.description
                }

                Write-Verbose "Prepare result"
                [pscustomobject]@{
                    $LocalPort           = $port
                    $ServiceName         = $name
                    $ServiceDescription  = $description
                }
                
            }
            Catch {
                # Print exception
                echo $($_.exception.message)
            }
        }
    }

    End {
        Write-Verbose "Ending $($CurrentConnection.list)"
    }
}