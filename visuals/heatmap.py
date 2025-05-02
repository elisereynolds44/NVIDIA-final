import plotly.graph_objects as go

def create_heatmap(corr_matrix):
    # is it missing
    if corr_matrix is None or corr_matrix.empty:
        return go.Figure(
            layout={
                "title": "Correlation matrix not available.",
                "xaxis": {"visible": False},
                "yaxis": {"visible": False}
            }
        )

    try:
        # extract labels from the axes from the matrix columns
        labels = corr_matrix.columns.tolist()

        # heatmap using plotly graph object
        fig = go.Figure(
            data=go.Heatmap(
                z=corr_matrix.values,
                x=labels,
                y=labels,
                colorscale='Viridis', # green-yellow-blue- gradient
                zmin=0,
                zmax=1
            )
        )

        # update chart layout w titles & axes labels 
        fig.update_layout(
            title='Stock Price Correlation Heatmap (2023 - 2024)',
            xaxis_title="Company",
            yaxis_title="Company"
        )
        return fig

    except Exception as e:
        print(f"Error creating heatmap: {e}")
        return go.Figure(
            layout={
                "title": "Error generating heatmap.",
                "xaxis": {"visible": False},
                "yaxis": {"visible": False}
            }
        )
