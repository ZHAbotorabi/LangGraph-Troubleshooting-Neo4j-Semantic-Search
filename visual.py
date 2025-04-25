# Reinstall required modules and regenerate visualization

# Since this environment has reset, re-create a static visualization manually
import graphviz

dot = graphviz.Digraph(comment="LangGraph Structure")

dot.node("ValidateQuery", "ValidateQuery")
dot.node("SemanticMatch", "SemanticMatch")
dot.node("GetProcedure", "GetProcedure")
dot.node("FetchDetails", "FetchDetails")
dot.node("BuildAnswer", "BuildAnswer")

dot.edge("ValidateQuery", "SemanticMatch")
dot.edge("SemanticMatch", "GetProcedure")
dot.edge("SemanticMatch", "FetchDetails")
dot.edge("GetProcedure", "BuildAnswer")
dot.edge("FetchDetails", "BuildAnswer")

dot.render("/mnt/data/langgraph_structure", format="png", cleanup=False)

"/mnt/data/langgraph_structure.png"
