# PDF Conversion

I iterated on a few options to convert the PDFs before settling on returning to the original Word `.doc` files as the source to create HTML output.

Converting PDFs is just still too icky - even with the advent of GenAI tech - the best I found was using Meta's Nougat tool but this was still resulting in quite a few glitches and no image extraction, although it handled the equations well.

---

## Process

1. Upload `.doc` files to Google Drive
2. Convert all docs there to Google Docs native format, rather than `.doc`
3. Download as Web Page, zipped, then unzip each
4. Format the one-line mega HTML output using VScode
5. Fix the `images/` references to `https://storage.googleapis.com/alchemyst-assets/docs/$type/$note_name/`
6. Strip the HTML header and body tags
7. Rename the HTML file to match the `doc_id` in this site's data store
8. Rename the local `images/` folder to `$note_name`
9. Use `copy.sh` below to copy Images to asset bucket and the document itself to `bootstrap` in this repo
10. Publish using When you're ready to make available, in the alchemyst repo:

    ```sh
    export DATA_STORE_NAMESPACE=Alchemyst
    export DATA_STORE_PROJECT=$GCP_PROJECT_ID
    pipenv run python bootstrap/documents/load_document.py
    ```

The app needs restarting to pick up the new content.

`copy.sh`:

```sh
#!/usr/bin/env bash
type=physical
cd ./exports/$type/ || exit
notes=$(ls -1 .)

for note in $notes; do
    doc_id=$(echo $note | awk -F- '{print $1}')
    note_name=$(echo $note | awk -F- '{print $2}')
    cd $note/ || exit
    cp ./$doc_id.html ~/alexos-dev/alchemyst/bootstrap/documents/
    if [[ -d $note_name/ ]]; then
        gsutil cp -r $note_name/ gs://alchemyst-assets/docs/$type/
    fi
    cd ../ || exit
done

cd ../../
```

---

## From PDF Attempts

1. `pipenv run nougat ./"${input}".pdf -o ./"${input}"/` produced pretty good results
2. `pandoc ./"${input}"/"${input}".tex -s -o ./"${input}"/"${input}"-tex.html --katex` on the output (afte renaming the output file to `.tex`) worked okay.
   - The `.mmd` can be converted to HTML with `multimarkdown ./"${input}"/"${input}".mmd -t html -o ./"${input}"/"${input}"-mmd.html` but this left the equations unformatted and I felt it was easier to fix bold/italics/headings in markdown than latex equations
3. Images can be extracted using `pdftohtml -c ./"${input}".pdf ./"${input}"/"${input}"-pdf.html`

In the end though, as noted above, when proofreading I did start to notice small errors in the Nougat output that put me off sufficiently to dig out the .doc file source material instead.
