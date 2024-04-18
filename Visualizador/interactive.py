import plotly.graph_objs as go


class InteractivePlot:
    @staticmethod
    def rel_entity_plot(df,  title:str ='Percentage Series Plot', drop_na:bool=False):

        if drop_na:
            df = df.dropna()

        data = []
        x_values = df.index

        for column in df.columns:
            trace = go.Scatter(
                x=x_values,
                y=df[column],
                mode='lines',
                name=column
            )
            data.append(trace)

        layout = go.Layout(
            title=title,
            xaxis=dict(title='Date'),
            yaxis=dict(title='Percentage'),
            legend=dict(traceorder='normal')
        )

        fig = go.Figure(data=data, layout=layout)
        fig.show(config={'scrollZoom': True, 'displayModeBar': True})

    @staticmethod
    def acum_entity_plot(df,drop_na=True):
        if drop_na:
            df = df.dropna()

        total = df[df.columns[0]]
        df = df.copy().drop(df.columns[0],axis=1)


        data = [go.Scatter(
                    x=total.index,
                    y=total,
                    mode='lines',
                    name=total.name
                )]
        x_values = df.index

        for i, column in enumerate(df.columns):
            trace = go.Scatter(
                    x=x_values,
                    y=df[column],
                    mode='lines',
                    name=column,
                    stackgroup='one'  # Stack on top of the previous column
                )
            data.append(trace)

        layout = go.Layout(
            title='Cumulative Flow Diagram',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Cumulative Percentage'),
            legend=dict(traceorder='normal')
        )

        fig = go.Figure(data=data, layout=layout)
        fig.show(config={'scrollZoom': True, 'displayModeBar': True})


if __name__ == '__main__':
    from BIE import Explorer
    e = Explorer()['Minería']['Volumen de producción minera por principales entidades federativas y municipios']['Oro']['Chihuahua']
    df = e.fetch()
    print(df)
    InteractivePlot.rel_entity_plot(df)
    InteractivePlot.acum_entity_plot(df)