from langgraph.graph import StateGraph, END
from app.models.state import PipelineState
from app.pipeline.nodes.jd_ingestion import jd_ingestion_node
from app.pipeline.nodes.portfolio_analysis import portfolio_analysis_node
from app.pipeline.nodes.skill_matching import skill_matching_node
from app.pipeline.nodes.doc_generation import doc_generation_node
from app.pipeline.nodes.qa_validation import qa_validation_node
from app.pipeline.nodes.post_apply import post_apply_node

def create_pipeline_graph():
    workflow = StateGraph(PipelineState)

    # Add Nodes
    workflow.add_node("ingest", jd_ingestion_node)
    workflow.add_node("analyze", portfolio_analysis_node)
    workflow.add_node("match", skill_matching_node)
    workflow.add_node("generate", doc_generation_node)
    workflow.add_node("validate", qa_validation_node)
    workflow.add_node("intel", post_apply_node)

def create_pipeline_graph():
    workflow = StateGraph(PipelineState)

    # Add Nodes
    workflow.add_node("ingest", jd_ingestion_node)
    workflow.add_node("analyze", portfolio_analysis_node)
    workflow.add_node("match", skill_matching_node)
    workflow.add_node("generate", doc_generation_node)
    workflow.add_node("validate", qa_validation_node)
    workflow.add_node("intel", post_apply_node)

def create_pipeline_graph():
    workflow = StateGraph(PipelineState)

    # Add Nodes
    workflow.add_node("ingest", jd_ingestion_node)
    workflow.add_node("analyze", portfolio_analysis_node)
    workflow.add_node("match", skill_matching_node)
    workflow.add_node("generate", doc_generation_node)
    workflow.add_node("validate", qa_validation_node)
    workflow.add_node("intel", post_apply_node)

    # Define Edges
    # Simple sequential flow to ensure stability
    workflow.set_entry_point("ingest")
    workflow.add_edge("ingest", "analyze")
    workflow.add_edge("analyze", "match")
    workflow.add_edge("match", "generate")
    workflow.add_edge("generate", "validate")
    workflow.add_edge("validate", "intel")
    workflow.add_edge("intel", END)

    return workflow.compile()

    return workflow.compile()

    return workflow.compile()

pipeline_app = create_pipeline_graph()
