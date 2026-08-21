# MT5 Preflight — Blocked

Date: 2026-08-21

The official `MetaTrader5` Python package was installed in the local runtime.
The read-only initialization attempt against:

`C:\Program Files\Hantec Markets MT5 Terminal\terminal64.exe`

did not return `account_info()` within 30 seconds. No order was sent and no
position or account state was changed by the attempt.

At verification time, two terminal processes were active:

- `C:\Program Files\MetaTrader 5\terminal64.exe`
- `C:\Program Files\Hantec Markets MT5 Terminal\terminal64.exe`

This is an unresolved runtime-session conflict. The DEMO test is not started
until the intended Hantec terminal session can be initialized and produce a
verified DEMO account response. No fake executor is being used as evidence of
this preflight.
