# Sentiment Analysis

- [sentistrengthn](http://sentistrength.wlv.ac.uk/): Tool for short text sentiment analysis.

## Linguistic Inquiry and Word Count (LIWC)

In order to be able to use LIWC, complete the following steps.

1. Purchase LIWC.
2. For LIWC 2015, the dictionary in the following .jar file in LIWC installation folder (e.g. `C:\Program Files (x86)\LIWC2015`): `\app\lib\LIWC2015-app-1.4.0.jar`.
    - You can open the jar file using WinRAR as an archive and find `LIWC2015_English_Flat.dic` in `com/liwc/LIWC2015/data/dict/`. 
    - Further info: [Issue 5 for LIWC2015](https://github.com/chbrown/liwc-python/issues/5)
3. Extract the `LIWC2015_English_Flat.dic` using WinRar (THIS FILE IS STILL ENCRYPTED).
4. Use the script `encrypting_liwc_dic.py` change in and output locations and `.jar` location to your directories.
5. Use the unencrypted file, such as in the uploaded example
   `liwc_analysis.py`.

Additional information can be found here: [LIWC](https://pypi.org/project/liwc/) and [Issue 3 for LIWC2015](https://github.com/chbrown/liwc-python/issues/3)
