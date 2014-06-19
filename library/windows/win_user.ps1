#!powershell
# This file is part of Ansible
#
# Copyright 2014, Paul Durivage <paul.durivage@rackspace.com>
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# WANT_JSON
# POWERSHELL_COMMON

$params = Parse-Args $args;

$result = New-Object psobject @{
    changed = false
};

If (-not $params.name.GetType)
{
    Fail-Json $result "missing required arguments: name"
}

If (-not $params.password.GetType)
{
    Fail-Json $result "missing required arguments: password"
}

$extra_args = $params "extra_args" "" 

If ($params.state) {
    $state = $params.state.ToString().ToLower()
    If (($state -ne 'present') -and ($state -ne 'absent')) {
        Fail-Json $result "state is '$state'; must be 'present' or 'absent'"
    }
}
Elseif (!$params.state) {
    $state = "present"
}

$username = Get-Attr $params "name"
$password = Get-Attr $params "password"

$user_obj = Get-User $username
if (-not $user_obj) {
    Fail-Json $result "Could not find user: $username"
}

if ($state -eq 'present') {
    # Add or update user
    try {
        if ($user_obj) {
            Update-Password $user_obj $password
        }
        else {
            Create-User $username $password
        }
        $result.changed = $true
    }
    catch {
        Fail-Json $result $_.Exception.Message
    }
    
}
else {
    # Remove user
    try {
        Delete-User $bob
        $result.changed = $true
    }
    catch {
        Fail-Json $result $_.Exception.Message
    }
}

$adsi = [ADSI]"WinNT://$env:COMPUTERNAME"

function Get-User($user) {
    $adsi.Children | where {$_.SchemaClassName -eq 'user' -and $_.Name -eq $user }
    return
}

function Create-User([string]$user, [string]$passwd) {
   $user = $adsi.Create("User", $user)
   $user.SetPassword($passwd)
   $user.SetInfo()
   $user
   return
}

function Update-Password($user, [string]$passwd) {
    $user.SetPassword($passwd)
    $user.SetInfo()
}

function Delete-User($user) {
    $adsi.delete("user", $user.Name.Value)
}

Set-Attr $result "user" $user_obj; # Soemthing goes here.

Exit-Json $result;
