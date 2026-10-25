# Daily quote collection

500 distinct quotes selected for a personal profile about computing, science,
mathematics, curiosity, learning, and invention. Each entry includes an author
and a source URL. The profile links the displayed author's name to that source.

## Sources and attribution

Most entries were selected from **English Wikiquote contributors**, with source
page revision links and the citations listed there retained in `quotes.json`.
The selection omits sections labelled unsourced, disputed, misattributed, and
quotes about the subject, and filters duplicates and unrelated material.

- Collection: https://en.wikiquote.org/
- Text compilation license: Creative Commons Attribution-ShareAlike 4.0,
  https://creativecommons.org/licenses/by-sa/4.0/
- Wikiquote copyright guidance: https://en.wikiquote.org/wiki/Wikiquote:Copyrights
- Changes: selected entries, removed formatting, normalized whitespace, and
  arranged authors into a daily rotation. The compiled selection is shared
  under the same CC BY-SA 4.0 terms. Underlying quotations retain their original
  copyright status; the compilation license does not change that status.

The initial short selection also includes quotes from:

- University of Toronto, Geoffrey Hinton's advice to students:
  https://www.utoronto.ca/news/follow-your-curiosity-geoffrey-hinton-offers-three-tips-incoming-students
- Computer History Museum, Alan Kay:
  https://www.computerhistory.org/revolution/story/315
- Alan Perlis's epigrams hosted by Yale:
  https://www.cs.yale.edu/homes/perlis-alan/quotes.html
- Paul Graham, *Hackers and Painters*:
  https://www.paulgraham.com/hp.html

Community citations are useful provenance, but all 500 quotations have not been
independently checked against original publications. Each record identifies
its verification status. Corrections can be made directly in `quotes.json`.

## Schedule

The GitHub workflow requests a run at **00:00 America/Toronto** every day,
including daylight-saving changes. GitHub can delay scheduled runs; this is
not a guarantee of a change at the exact second of midnight.

The updater uses the Toronto calendar date to choose a quote. Re-running on
the same date keeps the same quote; the collection repeats after 500 days.
Only the README text between the daily quote markers is changed.

The `Daily quote` workflow can also be run manually from the Actions page.
Uploading the workflow, updater, and quote file to `main` triggers its first run.
