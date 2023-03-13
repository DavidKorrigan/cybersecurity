<#
.SYNOPSIS
   Returns list of connections established.
.DESCRIPTION
   Returns list of connections established with IP owners.
.EXAMPLE
   Get-ConnectionEstablished
#>

function Get-ConnectionEstablished {
    [CmdletBinding()]
    [Alias()]
    [OutputType("List of Connections")]
    Param()

    Begin {
        Write-Verbose "Starting $($CurrentConnection.list)"

        # Get all the established connection on the host
        $connection = Get-NetTCPConnection -State Established

        # Prepare HTTP request
        $baseURL = "http://whois.arin.net/rest"
        $header = @{"Accept" = "application/xml"}

        # Prepare output label
        $RemoteIP = "Remote IP"
        $LocalPort = "Local Port"
        $IPOwner = "Remote IP Owner"
    }

    Process {
        # For each IP calls whois online service
        foreach($ip in $connection.RemoteAddress){
            Try {
                # Skip local IP
                if ($ip -ne "127.0.0.1") {
                    # Get detail on the current connection
                    $current_connection = Get-NetTCPConnection -RemoteAddress $ip

                    # Build the URL to call
                    $url = "$baseUrl/ip/$ip"

                    # Call the who is service
                    $r = Invoke-Restmethod $url -Headers $header -ErrorAction stop

                    Write-Verbose "Prepare result"
                    [pscustomobject]@{
                        $RemoteIP    = $ip
                        $LocalPort   = $current_connection.LocalPort
                        $IPOwner     = $r.net.orgRef.name
                    }
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