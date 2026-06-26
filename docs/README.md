# Source Documents

Put the personal documents you want to ingest here.

Supported target formats for the ingestion step:

- PDF files, for example `resume.pdf`
- Word files, for example `resume.docx`
- Plain text or Markdown files, for example `bio.md`

Recommended content:

- Resume
- Bio
- Skills
- Project descriptions
- Work experience
- Education
- Achievements

The ingestion pipeline will later:

1. Read files from this folder.
2. Extract text from each file.
3. Split the text into chunks with LangChain `RecursiveCharacterTextSplitter`.
4. Create OpenAI embeddings for each chunk.
5. Store the chunks and embeddings in ChromaDB.

This `README.md` file is ignored by the ingestion script.
