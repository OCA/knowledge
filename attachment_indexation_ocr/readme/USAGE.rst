By default, character recognition is done asynchronously by a cronjob at night.
This is because the recognition process takes a while and you don't want to make your users wait for the indexation to finish.
The interval to run the cronjob can be adjusted to your needs in the ``Scheduled Actions`` menu, under ` `Settings``.
In case you want to force the OCR to be done immediately, set configuration parameter ``ocr.synchronous`` to value ``True``.
