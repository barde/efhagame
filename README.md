Fachhochschule Kiel

Master Information Technology

Comp. Aspects of Game Programming

Made in 2012 by Bartholomäus Dedersen




﻿efhagame
======================================

Description:
------------

* This game is nuts
* Your aim is to watch your own brain's doing or click the graphic
* Turn off your soundcard
* Some requirements in hardware are needed for proper testing
* Soldering skills, too
* All correleation with existing things is purely coincidential or just happened by inspiration

Requirements
------------

So, at first you need a commercially available alarm clock which can be rebuit to a poor-man's
brainwave scanner.

You can buy it [here](http://goo.gl/qTycd) and support further actions on this attempt to use a 120$ device as you would
use your joystick. ;)

Next step is about accessing the Serial Debug Port on the back of your ZEO. _Attention:_ If you are not somewhat skilled with
and soldering iron you should ask somebody to do it for you. You can destroy your device or even machine!

[The instruction](http://zeorawdata.sourceforge.net/starting.html#interface-cable) can give you some hints.

Next go an install the firmware which allows direct access so you can do some magic with the included Python libary from former site.

Probably a SD-card with at least 4 MB, the download requires a [registration](http://developers.myzeo.com/raw-data-library/) and 
after a painless flashing procedure you can start using it.



Installation
------------

First you need to install [GIT](http://git-scm.com/) on your local host which is connected to the controlling node.
If you use Debian: `apt-get install git`

Afterwards you get the rolling-release version with:
`git clone git@github.com:barde/efhagame.git`

`cd efhagame` and `python game.py` should put up some kind of window with the game.

For playing 'pygame' must be installed. And if you insist in using the brain interface you should also install 'pyserial' and the [Zeo library](https://sourceforge.net/projects/zeorawdata/files/).
For Debian systems: `apt-get install python-pygame pyserial` and `wget http://downloads.sourceforge.net/project/zeorawdata/RDL2.0/ZeoRawData-2.0.zip`.
Read the included instructions for installing the ZeoRawData library.

If the included test program runs fine you are good to go. Otherwise use the source or check at first if you can access the ZEO directly with 'minicom' on your Serial adapter's port(probably '/dev/ttyUSB0').
   

Usage
------

Probably educational purposes as the png file is replaceable with whatever you desire.

We are still on getting some sample data to calibrate the brain interface.

Very Boring legal stuff
------------------

Copyright (c) 2012, Bartholomäus Dedersen

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Thanks
---------

[Phialo](http://www.phialo.de) - Phialo Graphix Design
[MyZeo](www.myzeo.com/) - ZEO Sleep quality measurement device(Look it up on [Amazon](http://goo.gl/qTycd))
