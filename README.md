# survey_with_chatbot
Tools for survey papers with chatbot

## Tools

### `pdf2txt_dir_tar_zip`

Converts every PDF file found inside a directory, tar archive, or zip archive
to a UTF-8 plain-text file, preserving the relative directory structure.

#### Installation

```bash
pip install .
```

#### Usage

```
pdf2txt_dir_tar_zip <input> <output>
```

| Argument | Accepted formats |
|----------|-----------------|
| `input`  | a directory, `.tar`, `.tar.gz`, `.tgz`, or `.zip` file containing PDFs |
| `output` | a directory path, `.tar`, `.tar.gz`, `.tgz`, or `.zip` file |

The output format is determined by the file extension of `<output>`.
Anything that does not end with a recognised archive extension is treated
as a directory (created automatically if it does not exist).

#### Examples

```bash
# Convert all PDFs in a local folder to text files in another folder
pdf2txt_dir_tar_zip papers/ texts/

# Convert PDFs packed in a zip archive; write results to a new zip
pdf2txt_dir_tar_zip papers.zip texts.zip

# Convert PDFs from a tar.gz; write results to a directory
pdf2txt_dir_tar_zip papers.tar.gz texts/
```
