"""gr.LinePlot() component"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, Callable, Literal

from gradio_client.documentation import document

from gradio.components.base import Component
from gradio.components.plot import AltairPlot, AltairPlotData, Plot
from gradio.events import Events

if TYPE_CHECKING:
    import pandas as pd

    from gradio.components import Timer

from gradio.events import Dependency

@document()
class LinePlot(Plot):
    """
    Creates a line plot component to display data from a pandas DataFrame (as output). As this component does
    not accept user input, it is rarely used as an input component.

    Demos: live_dashboard
    """

    data_model = AltairPlotData

    EVENTS = [Events.select]

    def __init__(
        self,
        value: pd.DataFrame | Callable | None = None,
        x: str | None = None,
        y: str | None = None,
        *,
        color: str | None = None,
        stroke_dash: str | None = None,
        overlay_point: bool | None = None,
        title: str | None = None,
        tooltip: list[str] | str | None = None,
        x_title: str | None = None,
        y_title: str | None = None,
        x_label_angle: float | None = None,
        y_label_angle: float | None = None,
        color_legend_title: str | None = None,
        stroke_dash_legend_title: str | None = None,
        color_legend_position: Literal[
            "left",
            "right",
            "top",
            "bottom",
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
            "none",
        ]
        | None = None,
        stroke_dash_legend_position: Literal[
            "left",
            "right",
            "top",
            "bottom",
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
            "none",
        ]
        | None = None,
        height: int | None = None,
        width: int | None = None,
        x_lim: list[int] | None = None,
        y_lim: list[int] | None = None,
        caption: str | None = None,
        label: str | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        every: Timer | float | None = None,
        inputs: Component | list[Component] | set[Component] | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
        show_actions_button: bool = False,
        interactive: bool | None = None,
    ):
        """
        Parameters:
            value: The pandas dataframe containing the data to display in a scatter plot.
            x: Column corresponding to the x axis. Can be grouped if datetime, e.g. 'yearmonth(date)' or 'minuteseconds(date)' with a column name 'date'. Any time unit supported by altair can be used.
            y: Column corresponding to the y axis. Can be aggregated, e.g. 'sum(price)' or 'count(price)' with a column name 'price'. Any aggregation function supported by altair can be used.
            color: The column to determine the point color. If the column contains numeric data, gradio will interpolate the column data so that small values correspond to light colors and large values correspond to dark values.
            stroke_dash: The column to determine the symbol used to draw the line, e.g. dashed lines, dashed lines with points.
            overlay_point: Whether to draw a point on the line for each (x, y) coordinate pair.
            title: The title to display on top of the chart.
            tooltip: The column (or list of columns) to display on the tooltip when a user hovers a point on the plot. Set to [] to disable tooltips.
            x_title: The title given to the x axis. By default, uses the value of the x parameter.
            y_title: The title given to the y axis. By default, uses the value of the y parameter.
            x_label_angle: The angle for the x axis labels. Positive values are clockwise, and negative values are counter-clockwise.
            y_label_angle: The angle for the y axis labels. Positive values are clockwise, and negative values are counter-clockwise.
            color_legend_title: The title given to the color legend. By default, uses the value of color parameter.
            stroke_dash_legend_title: The title given to the stroke_dash legend. By default, uses the value of the stroke_dash parameter.
            color_legend_position: The position of the color legend. If the string value 'none' is passed, this legend is omitted. For other valid position values see: https://vega.github.io/vega/docs/legends/#orientation.
            stroke_dash_legend_position: The position of the stoke_dash legend. If the string value 'none' is passed, this legend is omitted. For other valid position values see: https://vega.github.io/vega/docs/legends/#orientation.
            height: The height of the plot in pixels.
            width: The width of the plot in pixels. If None, expands to fit.
            x_lim: A tuple or list containing the limits for the x-axis, specified as [x_min, x_max].
            y_lim: A tuple of list containing the limits for the y-axis, specified as [y_min, y_max].
            caption: The (optional) caption to display below the plot.
            interactive: Deprecated.
            label: The (optional) label to display on the top left corner of the plot.
            show_label: Whether the label should be displayed.
            every: Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            inputs: Components that are used as inputs to calculate `value` if `value` is a function (has no effect otherwise). `value` is recalculated any time the inputs change.
            visible: Whether the plot should be visible.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
            show_actions_button: Whether to show the actions button on the top right corner of the plot.
        """
        self.x = x
        self.y = y
        self.color = color
        self.stroke_dash = stroke_dash
        self.tooltip = (
            tooltip if tooltip is not None else [elem for elem in [x, y, color] if elem]
        )
        self.title = title
        self.x_title = x_title
        self.y_title = y_title
        self.x_label_angle = x_label_angle
        self.y_label_angle = y_label_angle
        self.color_legend_title = color_legend_title
        self.stroke_dash_legend_title = stroke_dash_legend_title
        self.color_legend_position = color_legend_position
        self.stroke_dash_legend_position = stroke_dash_legend_position
        self.overlay_point = overlay_point
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.caption = caption
        if isinstance(width, str):
            width = None
            warnings.warn(
                "Width should be an integer, not a string. Setting width to None."
            )
        if isinstance(height, str):
            warnings.warn(
                "Height should be an integer, not a string. Setting height to None."
            )
            height = None
        self.width = width
        self.height = height
        self.show_actions_button = show_actions_button
        if label is None and show_label is None:
            show_label = False
        super().__init__(
            value=value,
            label=label,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            every=every,
            inputs=inputs,
        )
        if interactive is not None:
            warnings.warn(
                "The `interactive` parameter is deprecated and will be removed in a future version. "
                "The LinePlot component is always interactive."
            )

    def get_block_name(self) -> str:
        return "plot"

    @staticmethod
    def create_plot(
        value: pd.DataFrame,
        x: str,
        y: str,
        color: str | None = None,
        stroke_dash: str | None = None,
        overlay_point: bool | None = None,
        title: str | None = None,
        tooltip: list[str] | str | None = None,
        x_title: str | None = None,
        y_title: str | None = None,
        x_label_angle: float | None = None,
        y_label_angle: float | None = None,
        color_legend_title: str | None = None,
        stroke_dash_legend_title: str | None = None,
        color_legend_position: Literal[
            "left",
            "right",
            "top",
            "bottom",
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
            "none",
        ]
        | None = None,
        stroke_dash_legend_position: Literal[
            "left",
            "right",
            "top",
            "bottom",
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
            "none",
        ]
        | None = None,
        height: int | None = None,
        width: int | None = None,
        x_lim: list[int] | None = None,
        y_lim: list[int] | None = None,
    ):
        """Helper for creating the scatter plot."""
        import altair as alt

        encodings = {
            "x": alt.X(
                x,
                title=x_title or x,
                scale=AltairPlot.create_scale(x_lim),
                axis=alt.Axis(labelAngle=x_label_angle)
                if x_label_angle is not None
                else alt.Axis(),
            ),
            "y": alt.Y(
                y,
                title=y_title or y,
                scale=AltairPlot.create_scale(y_lim),
                axis=alt.Axis(labelAngle=y_label_angle)
                if y_label_angle is not None
                else alt.Axis(),
            ),
        }
        properties = {}
        if title:
            properties["title"] = title
        if height:
            properties["height"] = height
        if width:
            properties["width"] = width

        if color:
            color_legend_position = color_legend_position or "bottom"
            domain = value[color].unique().tolist()
            range_ = list(range(len(domain)))
            encodings["color"] = {
                "field": color,
                "type": "nominal",
                "scale": {"domain": domain, "range": range_},
                "legend": AltairPlot.create_legend(
                    position=color_legend_position, title=color_legend_title
                ),
            }

        if stroke_dash:
            stroke_dash_encoding = {
                "field": stroke_dash,
                "legend": AltairPlot.create_legend(
                    position=stroke_dash_legend_position or "bottom",
                    title=stroke_dash_legend_title,
                ),
            }
        else:
            stroke_dash_encoding = alt.value(alt.Undefined)

        if tooltip:
            encodings["tooltip"] = tooltip

        chart = alt.Chart(value).encode(**encodings)

        points = chart.mark_point(clip=True).encode(
            opacity=alt.value(alt.Undefined) if overlay_point else alt.value(0),
        )
        lines = chart.mark_line(clip=True).encode(strokeDash=stroke_dash_encoding)

        highlight = alt.selection_point(
            on="mouseover",
            fields=[c for c in [color, stroke_dash] if c],
            nearest=True,
            clear="mouseout",
            empty=False,
        )
        points = points.add_params(highlight)
        lines = lines.encode(
            size=alt.condition(highlight, alt.value(4), alt.value(2)),
        )
        if not overlay_point:
            highlight_pts = alt.selection_point(
                on="mouseover",
                nearest=True,
                clear="mouseout",
                empty=False,
            )
            points = points.add_params(highlight_pts)

            points = points.encode(
                opacity=alt.condition(highlight_pts, alt.value(1), alt.value(0)),
                size=alt.condition(highlight_pts, alt.value(100), alt.value(0)),
            )

        chart = (lines + points).properties(background="transparent", **properties)

        selection = alt.selection_interval(
            encodings=["x"],
            mark=alt.BrushConfig(fill="gray", fillOpacity=0.3, stroke="none"),
            name="brush",
        )
        chart = chart.add_params(selection)

        return chart

    def preprocess(self, payload: AltairPlotData | None) -> AltairPlotData | None:
        """
        Parameters:
            payload: The data to display in a line plot.
        Returns:
            (Rarely used) passes the data displayed in the line plot as an AltairPlotData dataclass, which includes the plot information as a JSON string, as well as the type of plot (in this case, "line").
        """
        return payload

    def postprocess(
        self, value: pd.DataFrame | dict | None
    ) -> AltairPlotData | dict | None:
        """
        Parameters:
            value: Expects a pandas DataFrame containing the data to display in the line plot. The DataFrame should contain at least two columns, one for the x-axis (corresponding to this component's `x` argument) and one for the y-axis (corresponding to `y`).
        Returns:
            The data to display in a line plot, in the form of an AltairPlotData dataclass, which includes the plot information as a JSON string, as well as the type of plot (in this case, "line").
        """
        # if None or update
        if value is None or isinstance(value, dict):
            return value
        if self.x is None or self.y is None:
            raise ValueError("No value provided for required parameters `x` and `y`.")
        chart = self.create_plot(
            value=value,
            x=self.x,
            y=self.y,
            color=self.color,
            overlay_point=self.overlay_point,
            title=self.title,
            tooltip=self.tooltip,
            x_title=self.x_title,
            y_title=self.y_title,
            x_label_angle=self.x_label_angle,
            y_label_angle=self.y_label_angle,
            color_legend_title=self.color_legend_title,  # type: ignore
            color_legend_position=self.color_legend_position,  # type: ignore
            stroke_dash_legend_title=self.stroke_dash_legend_title,
            stroke_dash_legend_position=self.stroke_dash_legend_position,  # type: ignore
            x_lim=self.x_lim,
            y_lim=self.y_lim,
            stroke_dash=self.stroke_dash,
            height=self.height,
            width=self.width,
        )

        return AltairPlotData(type="altair", plot=chart.to_json(), chart="line")

    def example_payload(self) -> Any:
        return None

    def example_value(self) -> Any:
        import pandas as pd

        return pd.DataFrame({self.x: [1, 2, 3], self.y: [4, 5, 6]})

    
    def select(self,
        fn: Callable | None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        outputs: Component | Sequence[Component] | None = None,
        api_name: str | None | Literal[False] = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: Timer | float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_api: bool = True) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: List of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: List of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: Defines how the endpoint appears in the API docs. Can be a string, None, or False. If False, the endpoint will not be exposed in the api docs. If set to None, the endpoint will be exposed in the api docs as an unnamed endpoint, although this behavior will be changed in Gradio 4.0. If set to a string, the endpoint will be exposed in the api docs with the given name.
            scroll_to_output: If True, will scroll to output component on completion
            show_progress: If True, will show progress animation while pending
            queue: If True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: If True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: Maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: If False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: If False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: A list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: Continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            trigger_mode: If "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: Optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: If set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: If set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            show_api: whether to show this event in the "view API" page of the Gradio app, or in the ".view_api()" method of the Gradio clients. Unlike setting api_name to False, setting show_api to False will still allow downstream apps as well as the Clients to use this event. If fn is None, show_api will automatically be set to False.
        """
        ...