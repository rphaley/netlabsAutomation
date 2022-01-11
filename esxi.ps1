#Created by Ryan Haley - DePaul University
$podNum = 7
$logon = Get-Content "esxi_settings.txt"
$vctr = $logon[2]

<#
$vms = "CSEC388_REG_POD{0}_*" -f $podNum
$dst = "CSEC388_POD{0}" -f $podNum
$net1 = "388POD{0}_INT" -f $podNum
$host1 = "CSEC388_REG_POD{0}_Kali" -f $podNum
$host2 = "CSEC388_REG_POD{0}_Windows*" -f $podNum
#>

<#
$vms = "CSEC388_FINAL_POD{0}_*" -f $podNum
$dst = "CSEC388_FINAL_POD{0}" -f $podNum
$net1 = "388FINALPOD{0}_INT" -f $podNum
$host1 = "CSEC388_FINAL_POD{0}_Kali" -f $podNum
$host2 = "CSEC388_FINAL_POD{0}_Windows*" -f $podNum
$net2 = "CSEC395_REG_POD{0}_EXT_VLAN546" -f $podNum
#>

$vms = "CSEC_395_POD{0}_*" -f $podNum
$dst = "CSEC395_POD{0}" -f $podNum
$net1 = "395POD{0}_INT" -f $podNum
$net2 = "395POD{0}_EXT_VLAN547" -f $podNum
$host1 = ""
$host2 = ""



Connect-VIServer -Server $vctr -User $logon[0] -Password $logon[1]
#Check VM list
get-vm $vms | fl Name
$ans = Read-Host -Prompt 'Are these the correct servers to modify (y/n)?'

if($ans -ne 'y') {
   return
}

#Move VMs to correct folder
get-vm  $vms | Move-VM -Destination $dst

#Revert to init snapshot
Get-Snapshot -VM $vms -Name init | Foreach-Object {
    Set-VM -VM $_.VM -Snapshot init  -RunAsync -Confirm:$false
}

#Change network adapters
get-vm  $vms | Get-NetworkAdapter -Name "Network adapter 1" | Set-NetworkAdapter -NetworkName $net1  -RunAsync -Confirm:$false
get-vm  $vms | Get-NetworkAdapter -Name "Network adapter 2" | Set-NetworkAdapter -NetworkName $net2  -RunAsync -Confirm:$false
if ($host1)
{get-vm  $host1 | Get-NetworkAdapter -Name "Network adapter 2" | Set-NetworkAdapter -NetworkName $net2  -RunAsync -Confirm:$false}
if ($host2)
{get-vm  $host2 | Get-NetworkAdapter -Name "Network adapter 2" | Set-NetworkAdapter -NetworkName $net2  -RunAsync -Confirm:$false}

#Delete snapshots
get-vm  $vms | Get-Snapshot | Remove-Snapshot -RunAsync -Confirm:$false
#Add new snapshot
get-vm  $vms |  New-Snapshot -Name init -RunAsync -Confirm:$false
