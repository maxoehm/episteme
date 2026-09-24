import * as echarts from "echarts/core";
import {
  LineChart,
  BarChart,
  PieChart,
  BoxplotChart,
  ScatterChart,
  HeatmapChart,
} from "echarts/charts";
import type {
  LineSeriesOption,
  BarSeriesOption,
  PieSeriesOption,
  BoxplotSeriesOption,
  ScatterSeriesOption,
  HeatmapSeriesOption,
} from "echarts/charts";
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DatasetComponent,
  VisualMapComponent,
} from "echarts/components";
import type {
  GridComponentOption,
  TooltipComponentOption,
  LegendComponentOption,
  TitleComponentOption,
  DatasetComponentOption,
  VisualMapComponentOption,
} from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([
  LineChart,
  BarChart,
  PieChart,
  BoxplotChart,
  ScatterChart,
  HeatmapChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DatasetComponent,
  VisualMapComponent,
  CanvasRenderer,
]);

export type EChartsOption = echarts.ComposeOption<
  | LineSeriesOption
  | BarSeriesOption
  | PieSeriesOption
  | BoxplotSeriesOption
  | ScatterSeriesOption
  | HeatmapSeriesOption
  | GridComponentOption
  | TooltipComponentOption
  | LegendComponentOption
  | TitleComponentOption
  | DatasetComponentOption
  | VisualMapComponentOption
>;

export * from "echarts/core";
