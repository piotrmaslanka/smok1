SMOK
====
(c) P.W. DMS s.c. 2009-2010

This is first version of SMOK system, written in 2009, in the era where it used an Atom server and a SOHO internet access with IP changing daily (no-ip rulez).

This was stripped of any corporate secrets in order to be posted online.

Please note that this is very legacy code, sinning plentifully against PEP8. This is only meant as a curiosity.

Waiting for release, in some very very far future, are SMOK2 and SMOK3. 

Current version, SMOK4, uses very elegant code and design, something entirely unlike it. Beware :>

Certain image files (c) Frisko.

My wild guesses as to what certain things are
=============================================

(please take a wide berth as I'm writing this after 10 years)

* [p24arch](p24arch) - current archives
* [24pazur](p24pazur) - this has been since axed from SMOK, this allowed users to run custom scripts on the target device. We're working to replicate this function in the upcoming *RAPID* line of modules. Usual case replaced with _timesynced_
* [patelnia](patelnia) and [afsensors](afsensors)- current runtime and core (approximately since these two libraries exchanged responsibilities multiple times)
* [p24server](p24server) - current Vesta for an older SSSP (P24)
* [afserver](afserver) - current SVCR, which then connected to Vesta via sockets, and not over AMQP
* [p24-frisko](p24-frisko) - this is a Tibbo program used to program DS1206 (at that time)
* [p24ip](p24ip) - a Django-written then-dynamite
* [afmotemote](afmotemote) - this is currently available only on-request, this allowed devices with MODBUS RTU over TCP to be integrated into SMOK as well (replaced TSM's KOLEKCJONER)
