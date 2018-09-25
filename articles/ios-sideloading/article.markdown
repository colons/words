# Nobody talks about sideloading apps on iOS

One of the oft-touted differences between Android and iOS is that Android lets you install apps from 'unknown sources', and iOS does not. This common knowledge is baked into almost all commentary written about mobile device security. For example, there was a lot of excitement after WWDC 2016 when Apple announced that free developer account certificates would be able to load apps onto iOS devices, but this is only for enrolled devices and the apps stop working after a week. There's also a lot of recent talk about Epic's decision to distribute Fortnite for Android outside of the Play Store, which is implicitly impossible with iOS.

![Screenshot. A native iOS prompt saying 'public.boxcloud.com would like to install “Snapchat++”'. The selectable options are 'Cancel' and 'Install'. 'Install' is the primary action, bold and blue. Behind the prompt, a website is visible, showing a summary of an app called 'Snapchat ++', authored by someone called 'Unknown'. Features offered include 'Increased Recording', 'Custom Notifications', and 'Enhanced screenshoting'](install.jpg)

The trouble is, though, that this premise is _catastrophically_ incorrect. Anyone can go to a website in Safari, download an app bundle, tap an 'Install' button in an alert that pops up, and the app will be installed. The first time you do this with an app from some rando, you'll also need to explicitly trust the signing authority in Settings. iOS won't tell you how to do this up-front, but it's not hard; certainly no harder than disabling Gatekeeper. No Mac is required, no developer account is required, and the app will run indefinitely. It's about as easy to do as enabling untrusted sources in Android.

This is not hypothetical. This is being done at volume in the wild.

![Screenshot. The iOS settings app. Explanatory text says 'Apps from developer “iPhone Distribution: Shenzhen Yunxun Technology Co., Ltd.” are not trusted on this iPad and will not run until the developer is trusted.' Beneath this text, there's an inviting blue button labelled 'Trust “Shenzhen Yunxun Technology Co., Ltd.”', and then there's a list of apps that are signed by this entity. The only item in the list is 'Twitter ++', an app that uses the official Twitter app icon. Opposite the name of the app, the word 'Verified' is shown.](trust.jpg)

There's a website called BuildStore which sells subscriptions for access to their database of apps that can be installed this way, including open-source emulators and modified versions of apps like Facebook with 'additional features'. Scarier, though, are the places that offer this for free, like iEmulators. Given the cost of hosting and the inherent price of the ability to offer this service (which we'll get into in a bit), it seems reasonable to assume that the people running this free service are expecting to make a profit, somehow.

BuildStore's practice of selling access to other people's open-source software is questionable, but the ['improved' social media apps category][iemulators-tutorial] offered by iEmulators is _terrifying_. I am not equipped to disassemble an iOS app and work out what it does, and I don't want to make accusations about any specific application distributors, but if I was the 'Unknown' person who distributes these [social media website]++ apps and I wanted to make money unscrupulously, I know some things that I would do. I'd sell ads and send you paid notifications. I'd use all the compute time I could get to mine cryptocurrency. I'd record everything you did in the app. Once you granted camera permissions, I would never turn them off. Once you granted access to your photos library, I would use EXIF data to build a history of everywhere memorable you've ever been. I'd use each and every API that Apple don't allow to be used in apps distributed in the App Store to gather as much personal information about you as possible, and I'd sell all of it. I'd also, naturally, gather your login credentials.

Twitter ++, which I briefly ran on a wiped device to see what it was like, injects ads into the signup process in a slick-enough way that there is clearly some serious technical skill behind these apps. I have no doubt that much of the rest of the above is being done, too.

----

BuildStore requires the unique identifier of enrolled iOS devices, which almost certainly means they're just [signing][code-signing] apps with developer provisioning profiles, rather than using [TestFlight][testflight] or the [Volume Purchase Program store][b2b] for their review-free distribution. I am unwilling to pay them to confirm this. The unrestricted distribution that free sites like iEmulators are able to do, however, is made possible by the [Apple Developer Enterprise Program][enterprise].

With the Apple Developer Enterprise Program, for $300 per year, you get to distribute apps to as many devices as you like. According to [their license agreement][enterprise-la], use of your apps on these devices should be:

> (i) on Your physical premises and/or on Your Permitted Entity’s physical premises, or (ii) in other locations, provided all such use is under the direct supervision and physical control of Your Employees or Permitted Users (e.g., a sales presentation to a Customer)

The agreement goes on to explain that posting enterprise-signed apps on a public website is explicitly prohibited. Clearly, this is not being enforced, at least not particularly rigorously.

In theory, though, this should be fine! In theory, iOS is a reasonably secure operating system, and all apps have to ask permission to get access to sensitive information. In theory, there's no reason iOS couldn't safely host arbitrary apps and still be orders of magnitude safer than macOS. You can't stop stuff like cryptocurrency miners, but you can at least stop invasive fingerprinting and data gathering. In theory.

App Store review is supposed to be an important protection here. Their automated reviews will catch use of private APIs and such, but there's a lot that the humans don't catch. iOS still contains a bunch of mechanisms apps can use to do malicious things that _should_ be prevented by App Store policies and review, but aren't. People have been doing [pretty][app-graph] [shady][facebook-audio] [stuff][path] on the App Store for years now, and Apple only reliably remedies it once it's already a story. In the meantime, they'll arbitrarily reject any app that a given reviewer has a [political][liyla], [social][happy-playtime], [financial][steam-link], or [functional][pythonista] objection to, and be [stubbornly uncommunicative][dash] about it until enough people or press outlets get mad about it.

----

So why don't Epic use enterprise certificates for Fortnite? ‘Obviously,’ I hear you cry, ‘it's against the terms, so Epic's enterprise certificate would get revoked immediately if they tried to distribute Fortnite outside of the App Store,’ and you're right. Such a flagrantly contract-violating move for such a popular app from a big company would get massive press coverage, and be shut down within hours. If Apple's primary concern here was security, though, Epic's certificate would be the least of their worries. Apple know damn well that Epic's not going to distribute malware, and we know that the primary reason they want to keep stuff in the App Store is for [that hot 30% revenue cut][steam-link]. The long-term existence of third-party iOS malware distribution sites should hammer this past the point of deniability, but everyone covering these platforms either ignores their existence or, worse, doesn't know about them.

iOS is living in the worst of both worlds. Nobody acting above board is allowed to distribute apps outside of Apple's control, but there's a thriving market of independently-distributed malware that nobody talks about. It would be nice if at least one of these downsides could be eliminated.

[app-graph]: https://techcrunch.com/2014/11/26/twitter-app-graph/
[b2b]: https://developer.apple.com/programs/volume/b2b/
[code-signing]: https://developer.apple.com/support/code-signing/
[dash]: https://blog.kapeli.com/apple-removed-dash-from-the-app-store
[developer-program]: https://developer.apple.com/programs/
[enterprise]: https://developer.apple.com/programs/enterprise/
[enterprise-la]: https://download.developer.apple.com/Documentation/License_Agreements__Apple_Developer_Enterprise_Program/Apple_Developer_Enterprise_Program_License_Agreement_20180604.pdf
[facebook-audio]: https://medium.com/@mg/battery-life-load-times-and-actually-giving-a-shit-about-your-customers-c3738386bded
[flux]: https://justgetflux.com/sideload/
[happy-playtime]: https://www.dailydot.com/debug/female-masturbation-app-apple/
[iemulators-tutorial]: https://www.youtube.com/watch?v=pzoImYUXz0E
[liyla]: https://www.polygon.com/2016/5/20/11723856/apple-palestinian-game-rejection-liyla-and-the-shadows-of-war
[notarisation]: https://developer.apple.com/videos/play/wwdc2018/702/
[path]: https://www.theverge.com/2012/2/7/2782947/path-ios-app-user-information-collected-privacy
[pythonista]: https://mjtsai.com/blog/2014/06/12/pythonista-in-app-store-peril/
[steam-link]: https://toucharcade.com/2018/06/14/valve-updates-steam-link-ios-app-to-remove-game-purchasing/
[testflight]: https://developer.apple.com/testflight/
