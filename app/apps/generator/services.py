from app.apps.generator.schema import InGenerator, Reference, GeneratorSchema

from app.configurations import rag_chain


class GeneratorService():
    def __init__(self) -> None:
        pass

    async def run(self, in_query_schema: InGenerator) -> GeneratorSchema:
        response = rag_chain.invoke(
            {"input": in_query_schema.query}
        )
        references = []

        for ref in response["context"]:
            references.append(Reference(
                link=ref.metadata["source"],
                text=ref.page_content,
                # when loaded documents page count started from 0
                page=ref.metadata["page"] + 1,
            ))

        return GeneratorSchema(answer=response["answer"], references=references)
