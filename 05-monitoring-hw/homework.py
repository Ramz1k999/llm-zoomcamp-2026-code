from dotenv import load_dotenv

load_dotenv()

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from exporter import SQLiteSpanExporter

provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(SQLiteSpanExporter("traces.db"))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("llm-zoomcamp")


from starter import rag as base_rag

from rag_helper import RAGBase

class RAGTraced(RAGBase):

    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search") as span:
            results = self.index.search(
                query,
                num_results=num_results,
                boost_dict={},
            )
            span.set_attribute("num_results", len(results))
            return results

    def build_context(self, search_results):
        lines = []
        for doc in search_results:
            lines.append(doc['filename'])
            lines.append(doc['content'])
            lines.append('')
        return '\n'.join(lines).strip()

    def llm(self, prompt):
        with tracer.start_as_current_span("llm") as span:
            input_messages = [
                {'role': 'developer', 'content': self.instructions},
                {'role': 'user', 'content': prompt}
            ]
            response = self.llm_client.responses.create(
                model=self.model,
                input=input_messages
            )
            usage = response.usage
            span.set_attribute("input_tokens", usage.input_tokens)
            span.set_attribute("output_tokens", usage.output_tokens)
            return response.output_text

    def rag(self, query):
        with tracer.start_as_current_span("rag") as span:
            return super().rag(query)

rag = RAGTraced(index=base_rag.index, llm_client=base_rag.llm_client)

if __name__ == "__main__":
    query = "How does the agentic loop keep calling the model until it stops?"
    answer = rag.rag(query)

    print("\n--- Ответ от модели ---")
    print(answer)