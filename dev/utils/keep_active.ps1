$wshell = New-Object -ComObject Wscript.Shell
Write-Host "アクティブ維持スクリプト起動中... (Ctrl+C で停止)"
while ($true) {
    # ScrollLock キーを2回押して状態を元に戻しつつアクティブを維持
    $wshell.SendKeys("{SCROLLLOCK}")
    Start-Sleep -Milliseconds 100
    $wshell.SendKeys("{SCROLLLOCK}")
    
    Start-Sleep -Seconds 10
}