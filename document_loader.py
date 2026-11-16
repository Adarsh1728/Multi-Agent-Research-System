
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document


def load_uploaded_files(uploaded_files):
    documents = []

    for uploaded in uploaded_files:
        try:
            filename = uploaded.name
            extension = Path(filename).suffix.lower()
            file_data = uploaded.getvalue()

            if extension == ".pdf":
                reader = PdfReader(BytesIO(file_data))

                for page_number, page in enumerate(reader.pages, start=1):
                    text = page.extract_text() or ""

                    if text.strip():
                        documents.append(
                            Document(
                                page_content=text,
                                metadata={
                                    "source": filename,
                                    "page": page_number
                                }
                            )
                        )

            elif extension in [".txt", ".md"]:
                text = file_data.decode("utf-8", errors="ignore")

                if text.strip():
                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": filename,
                                "page": 1
                            }
                        )
                    )

            else:
                raise ValueError(f"Unsupported file: {filename}")

        except Exception as e:
            raise RuntimeError(
                f"Failed to process {uploaded.name}: {e}"
            ) from e

    return documents
