# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

replot = undefined
updateRangeInput = undefined
updateTextInput = undefined
replot = (results) ->
  y.domain [
    0
    document.getElementById("yMaxInput").value
  ]
  y2.domain y.domain()
  focus.selectAll(".area").data(results).attr("id", (d) ->
    d[0].orbital
  ).attr("class", (d) ->
    t = undefined
    t = parseInt(d[0].orbital.substring(2, 3))
    switch t
      when 0
        "area orb class s"
      when 1
        "area orb class p"
      when 2
        "area orb class d"
  ).attr "d", area
  focus.call(yAxis).append("g").attr("class", "y axis").call yAxis
  context.selectAll(".area").data(results).attr("id", (d) ->
    d[0].orbital
  ).attr("class", (d) ->
    t = undefined
    t = parseInt(d[0].orbital.substring(2, 3))
    switch t
      when 0
        "area orb class s"
      when 1
        "area orb class p"
      when 2
        "area orb class d"
  ).attr "d", area2
  return

updateTextInput = (val) ->
  val = 0.1  if val < 0.1
  document.getElementById("yMaxInput").value = val
  replot results
  return

updateRangeInput = (val) ->
  val = 0.1  if val < 0.1
  document.getElementById("yMaxRange").value = val
  replot results
  return

dosPlot = (results) ->
  x.domain [
    -15
    4
  ]
  y.domain [
    0
    document.getElementById("yMaxInput").value
  ]
  x2.domain x.domain()
  y2.domain y.domain()
  focus.selectAll(".area").data(results).enter().append("path").attr("id", (d) ->
    d[0].orbital
  ).attr("class", (d) ->
    t = parseInt(d[0].orbital.substring(2, 3))
    switch t
      when 0
        "area orb class s"
      when 1
        "area orb class p"
      when 2
        "area orb class d"
  ).attr "d", area
  focus.append("g").attr("class", "x axis").attr("transform", "translate(0," + height + ")").call xAxis
  focus.append("g").attr("class", "y axis").call yAxis
  context.selectAll(".area").data(results).enter().append("path").attr("id", (d) ->
    d[0].orbital
  ).attr("class", (d) ->
    t = parseInt(d[0].orbital.substring(2, 3))
    switch t
      when 0
        "area orb class s"
      when 1
        "area orb class p"
      when 2
        "area orb class d"
  ).attr "d", area2
  context.append("g").attr("class", "x axis").attr("transform", "translate(0," + height2 + ")").call xAxis2
  context.append("g").attr("class", "x brush").call(brush).selectAll("rect").attr("y", -6).attr "height", height2 + 7
  return
brushed = ->
  x.domain (if brush.empty() then x2.domain() else brush.extent())
  focus.selectAll(".area").attr "d", area
  focus.select(".x.axis").call xAxis
  return
margin =
  top: 10
  right: 10
  bottom: 100
  left: 40

margin2 =
  top: 430
  right: 10
  bottom: 20
  left: 40

width = 960 - margin.left - margin.right
height = 500 - margin.top - margin.bottom
height2 = 500 - margin2.top - margin2.bottom
x = d3.scale.linear().range([
  0
  width
])
x2 = d3.scale.linear().range([
  0
  width
])
y = d3.scale.linear().range([
  height
  0
])
y2 = d3.scale.linear().range([
  height2
  0
])
xAxis = d3.svg.axis().scale(x).orient("bottom")
xAxis2 = d3.svg.axis().scale(x2).orient("bottom")
yAxis = d3.svg.axis().scale(y).orient("left")
brush = d3.svg.brush().x(x2).on("brush", brushed)
svg = d3.select("#chart").append("svg:svg").attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom)
area = d3.svg.area().interpolate("monotone").x((d) ->
  x d.x
).y0(height).y1((d) ->
  y d.y
)
area2 = d3.svg.area().interpolate("monotone").x((d) ->
  x2 d.x
).y0(height2).y1((d) ->
  y2 d.y
)
svg.append("defs").append("clipPath").attr("id", "clip").append("rect").attr("width", width).attr "height", height
focus = svg.append("g").attr("class", "focus").attr("transform", "translate(" + margin.left + "," + margin.top + ")")
context = svg.append("g").attr("class", "context").attr("transform", "translate(" + margin2.left + "," + margin2.top + ")")


$(document).ready ->
  $("#selectall").click (event) -> #on click
    if @checked # check select status
      $(".checkbox").each -> #loop through each checkbox
        @checked = true
        return

      svg.selectAll(".orb").style "display", null
    else
      $(".checkbox").each -> #loop through each checkbox
        @checked = false
        return

      svg.selectAll(".orb").style "display", "none"
    return

  return
