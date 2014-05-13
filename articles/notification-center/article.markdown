# I don't use Notification Center, and it makes me sad

As an Android and OS X user, I was excited when Apple announced that they were
going to integrate something resembling [Growl][growl] into [Mountain
Lion][ars]. Growl was, at the time, a surprisingly critical part of the OS X
ecosystem. Apple bringing Growl's responsibilities in-house seemed long
overdue.

Unfortunately, since a couple of days after Mountain Lion was released, I have
barely touched Notification Center. What follows is an attempt to rationalise
exactly why that is.

----

## Action

One of my favourite things about Android's notifications are that if I get an
email that I do not have to act on, I can archive it right from the
notification. I use this a lot.

Notification Center's transient notifications recently got similar little
buttons added to them. You can reply to an email *right there*, provided you
decide to act on it and can get your mouse up to the button within five seconds
of the notification appearing. If you miss this opportunity, you are out of
luck, because the persistent versions of notifications do not retain these
buttons.

## Persistence

When you have pending notifications on Android, it's like a splinter. You *can*
ignore them, and if you are busy, you can even forget they're there, but you
won't feel right until they're gone.

As an example, here's before:

![lots of notifications](android-full.png)

And after:

![phew](android-empty.png)

Feels better, right? You now know, without taking any action, that there's
nothing left for you to deal with right now. And everything is tidy.

Here's Notification Center's entire visible UI when you have notifications
pending:

![lots of notifications?](osx-full.png)

And when you do not:

![oh](osx-empty.png)

Nothing changes.

Notification Center doesn't get back to you when you are no longer busy; *you*
have to get back to *it*. There is zero motivation to look in the slide-out
drawer unless you already know there's something there because you saw it
earlier and made a note of it.

That bears repeating. This *notification system* requires you to remember that
a notification appeared while you were busy (or briefly on the other side of
the room) and follow up on it. Like an animal.

## Retention

…so it goes unchecked. Notifications come in, and stay in, and will stay there
until you dismiss them.

Except that's not true at all. What actually happens is that each app has a
rotating collection of the five most recent notifications they emitted. If you
get a lot of emails, Notification Center is useless for triage. If you get a
lot of tweets, Notification Center is useless for sampling. In all cases I've
encountered, the app that spawned the notification is a superior tool for
catching up on things. Further, most of them have icon badges or menu bar
widgets to constantly remind you that something is worth your attention, making
Notification Center entirely redundant.

## Dismissal

Every now and then, though, I accidentally open the drawer when trying to
scroll or something, and I get wistful. I look at countless notifications for
things I have *already dealt with* and I think of what could have been. I look
mournfully at my phone, sigh, and dutifully click all the tiny X buttons.

[growl]: https://en.wikipedia.org/wiki/Growl_%28software%29
[ars]: http://arstechnica.com/apple/2012/07/os-x-10-8/4/#notification-center
