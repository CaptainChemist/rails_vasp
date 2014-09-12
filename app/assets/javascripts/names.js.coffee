# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

replot = (results) ->
  y.domain [
    0
    document.getElementById("yMaxInput").value
  ]
  y2.domain y.domain()
  focus.selectAll(".area").data(results).attr("id", (d) ->
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
  focus.call(yAxis).append("g").attr("class", "y axis").call yAxis
  context.selectAll(".area").data(results).attr("id", (d) ->
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
  context.call(yAxis2).append("g").selectAll("rect").attr("y", -6).attr "height", height2 + 7
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


replot = (results) ->
  y.domain [
    0
    document.getElementById("yMaxInput").value
  ]
  y2.domain y.domain()
  focus.selectAll(".area").data(results).attr("id", (d) ->
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
  focus.call(yAxis).append("g").attr("class", "y axis").call yAxis
  context.selectAll(".area").data(results).attr("id", (d) ->
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
  context.call(yAxis2).append("g").selectAll("rect").attr("y", -6).attr "height", height2 + 7
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
