import winreg
import wmi

ip = "10.139.2.105"
username = "DVT-SECAS-016\\administrator"
password = "Welcome1"

c = wmi.WMI(computer=ip, user=username,
password=password,namespace="root/default").StdRegProv


result, names, data = c.EnumValues (
  sSubKeyName="SOFTWARE\WOW6432Node\Microsoft\RADAR\CommitExhaustion\Settings"
)

for item in names:
    print(c.GetDWORDValue(sSubKeyName="SOFTWARE\WOW6432Node\Microsoft\RADAR\CommitExhaustion\Settings", sValueName=item)[1])