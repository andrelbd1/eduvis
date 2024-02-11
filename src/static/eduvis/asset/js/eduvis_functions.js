function buildingDashboard(title,chartPlotlyId,chartId,customizable) {
  var colNode1 = document.createElement("div");
  var colNode1att1 = document.createAttribute("class");
  var colNode1att2 = document.createAttribute("style");
  colNode1att1.value = "col-md-12";
  colNode1att2.value = "padding:5px;";
  colNode1.setAttributeNode(colNode1att1);
  colNode1.setAttributeNode(colNode1att2);

  var colNode2 = document.createElement("div");
  var colNode2att1 = document.createAttribute("class");
  colNode2att1.value = "col-md-12";
  colNode2.setAttributeNode(colNode2att1);
  
  var panel1 = document.createElement("div");
  var panel1att1 = document.createAttribute("class");
  panel1att1.value = "panel";
  panel1.setAttributeNode(panel1att1);

  var panelHeading = document.createElement("div");
  var panelHeadingatt1 = document.createAttribute("class");
  var panelHeadingatt2 = document.createAttribute("style");
  panelHeadingatt1.value = "panel-heading bg-white border-none";
  panelHeadingatt2.value = "padding:50px;";
  panelHeading.setAttributeNode(panelHeadingatt1);
  panelHeading.setAttributeNode(panelHeadingatt2);
  
  var colNode3 = document.createElement("div");
  var colNode3att1 = document.createAttribute("class");
  colNode3att1.value = "col-md-8 col-sm-8 col-sm-12 text-left";
  colNode3.setAttributeNode(colNode3att1);

  var titleNode = document.createElement("h4");
  var titleNodeBold = document.createElement("b");
  var textTitleNode = document.createTextNode(title);

  var colNode4 = document.createElement("div");
  var colNode4att1 = document.createAttribute("class");
  colNode4att1.value = "col-md-4 col-sm-4 col-sm-12 text-right";
  colNode4.setAttributeNode(colNode4att1);              

  var buttonMoveTop = document.createElement("button");
  var buttonMoveTopatt1 = document.createAttribute("class");
  var buttonMoveTopatt2 = document.createAttribute("data-toggle");
  var buttonMoveTopatt3 = document.createAttribute("data-placement");
  var buttonMoveTopatt4 = document.createAttribute("title");
  var buttonMoveTopatt5 = document.createAttribute("value");
  var buttonMoveTopatt6 = document.createAttribute("onclick");
  buttonMoveTopatt1.value = "btn btn-outline btn-mn btn-lg btn-primary";
  buttonMoveTopatt2.value = "tooltip";
  buttonMoveTopatt3.value = "bottom";
  buttonMoveTopatt4.value = "Mover para o topo";
  buttonMoveTopatt5.value = "primary";
  buttonMoveTopatt6.value = "moveTopItemDashboard(this,'"+chartId+"')";
  buttonMoveTop.setAttributeNode(buttonMoveTopatt1);
  buttonMoveTop.setAttributeNode(buttonMoveTopatt2);
  buttonMoveTop.setAttributeNode(buttonMoveTopatt3);
  buttonMoveTop.setAttributeNode(buttonMoveTopatt4);
  buttonMoveTop.setAttributeNode(buttonMoveTopatt5);
  buttonMoveTop.setAttributeNode(buttonMoveTopatt6);

  var spanButtonMoveTop = document.createElement("span");
  var spanButtonMoveTopatt1 = document.createAttribute("class");
  spanButtonMoveTopatt1.value = "fa fa-angle-double-up";
  spanButtonMoveTop.setAttributeNode(spanButtonMoveTopatt1);

  var buttonMoveUp = document.createElement("button");
  var buttonMoveUpatt1 = document.createAttribute("class");
  var buttonMoveUpatt2 = document.createAttribute("data-toggle");
  var buttonMoveUpatt3 = document.createAttribute("data-placement");
  var buttonMoveUpatt4 = document.createAttribute("title");
  var buttonMoveUpatt5 = document.createAttribute("value");
  var buttonMoveUpatt6 = document.createAttribute("onclick");
  buttonMoveUpatt1.value = "btn btn-outline btn-mn btn-lg btn-primary";
  buttonMoveUpatt2.value = "tooltip";
  buttonMoveUpatt3.value = "bottom";
  buttonMoveUpatt4.value = "Mover para cima";
  buttonMoveUpatt5.value = "primary";
  buttonMoveUpatt6.value = "moveUpItemDashboard(this,'"+chartId+"')";
  buttonMoveUp.setAttributeNode(buttonMoveUpatt1);
  buttonMoveUp.setAttributeNode(buttonMoveUpatt2);
  buttonMoveUp.setAttributeNode(buttonMoveUpatt3);
  buttonMoveUp.setAttributeNode(buttonMoveUpatt4);
  buttonMoveUp.setAttributeNode(buttonMoveUpatt5);
  buttonMoveUp.setAttributeNode(buttonMoveUpatt6);

  var spanButtonMoveUp = document.createElement("span");
  var spanButtonMoveUpatt1 = document.createAttribute("class");
  spanButtonMoveUpatt1.value = "fa fa-angle-up";
  spanButtonMoveUp.setAttributeNode(spanButtonMoveUpatt1);
  
  var buttonMoveDown = document.createElement("button");
  var buttonMoveDownatt1 = document.createAttribute("class");
  var buttonMoveDownatt2 = document.createAttribute("data-toggle");
  var buttonMoveDownatt3 = document.createAttribute("data-placement");
  var buttonMoveDownatt4 = document.createAttribute("title");
  var buttonMoveDownatt5 = document.createAttribute("value");
  var buttonMoveDownatt6 = document.createAttribute("onclick");
  buttonMoveDownatt1.value = "btn btn-outline btn-mn btn-lg btn-primary";
  buttonMoveDownatt2.value = "tooltip";
  buttonMoveDownatt3.value = "bottom";
  buttonMoveDownatt4.value = "Mover para baixo";
  buttonMoveDownatt5.value = "primary";
  buttonMoveDownatt6.value = "moveDownItemDashboard(this,'"+chartId+"')";
  buttonMoveDown.setAttributeNode(buttonMoveDownatt1);
  buttonMoveDown.setAttributeNode(buttonMoveDownatt2);
  buttonMoveDown.setAttributeNode(buttonMoveDownatt3);
  buttonMoveDown.setAttributeNode(buttonMoveDownatt4);
  buttonMoveDown.setAttributeNode(buttonMoveDownatt5);
  buttonMoveDown.setAttributeNode(buttonMoveDownatt6);

  var spanButtonMoveDown = document.createElement("span");
  var spanButtonMoveDownatt1 = document.createAttribute("class");
  spanButtonMoveDownatt1.value = "fa fa-angle-down";
  spanButtonMoveDown.setAttributeNode(spanButtonMoveDownatt1);

  var buttonMoveBottom = document.createElement("button");
  var buttonMoveBottomatt1 = document.createAttribute("class");
  var buttonMoveBottomatt2 = document.createAttribute("data-toggle");
  var buttonMoveBottomatt3 = document.createAttribute("data-placement");
  var buttonMoveBottomatt4 = document.createAttribute("title");
  var buttonMoveBottomatt5 = document.createAttribute("value");
  var buttonMoveBottomatt6 = document.createAttribute("onclick");
  buttonMoveBottomatt1.value = "btn btn-outline btn-mn btn-lg btn-primary";
  buttonMoveBottomatt2.value = "tooltip";
  buttonMoveBottomatt3.value = "bottom";
  buttonMoveBottomatt4.value = "Mover para a base";
  buttonMoveBottomatt5.value = "primary";
  buttonMoveBottomatt6.value = "moveBottomItemDashboard(this,'"+chartId+"')";
  buttonMoveBottom.setAttributeNode(buttonMoveBottomatt1);
  buttonMoveBottom.setAttributeNode(buttonMoveBottomatt2);
  buttonMoveBottom.setAttributeNode(buttonMoveBottomatt3);
  buttonMoveBottom.setAttributeNode(buttonMoveBottomatt4);
  buttonMoveBottom.setAttributeNode(buttonMoveBottomatt5);
  buttonMoveBottom.setAttributeNode(buttonMoveBottomatt6);

  var spanButtonMoveBottom = document.createElement("span");
  var spanButtonMoveBottomatt1 = document.createAttribute("class");
  spanButtonMoveBottomatt1.value = "fa fa-angle-double-down";
  spanButtonMoveBottom.setAttributeNode(spanButtonMoveBottomatt1);

  var buttonSettings = document.createElement("button");
  var buttonSettingsatt1 = document.createAttribute("class");
  var buttonSettingsatt2 = document.createAttribute("data-toggle");
  var buttonSettingsatt3 = document.createAttribute("data-placement");
  var buttonSettingsatt4 = document.createAttribute("title");
  var buttonSettingsatt5 = document.createAttribute("value");
  var buttonSettingsatt6 = document.createAttribute("onclick");
  buttonSettingsatt1.value = "btn btn-outline btn-mn btn-lg btn-primary";
  buttonSettingsatt2.value = "tooltip";
  buttonSettingsatt3.value = "bottom";
  buttonSettingsatt4.value = "Configurações do tópico";
  buttonSettingsatt5.value = "primary";
  buttonSettingsatt6.value = "settingsItemDashboard('"+chartId+"')";
  buttonSettings.setAttributeNode(buttonSettingsatt1);
  buttonSettings.setAttributeNode(buttonSettingsatt2);
  buttonSettings.setAttributeNode(buttonSettingsatt3);
  buttonSettings.setAttributeNode(buttonSettingsatt4);
  buttonSettings.setAttributeNode(buttonSettingsatt5);
  buttonSettings.setAttributeNode(buttonSettingsatt6);

  var spanButtonSettings = document.createElement("span");
  var spanButtonSettingsatt1 = document.createAttribute("class");
  spanButtonSettingsatt1.value = "fa fa-cogs";
  spanButtonSettings.setAttributeNode(spanButtonSettingsatt1);

  var buttonRemove = document.createElement("button");
  var buttonRemoveatt1 = document.createAttribute("class");
  var buttonRemoveatt2 = document.createAttribute("data-toggle");
  var buttonRemoveatt3 = document.createAttribute("data-placement");
  var buttonRemoveatt4 = document.createAttribute("title");
  var buttonRemoveatt5 = document.createAttribute("value");
  var buttonRemoveatt6 = document.createAttribute("onclick");
  buttonRemoveatt1.value = "btn btn-outline btn-mn btn-lg btn-primary";
  buttonRemoveatt2.value = "tooltip";
  buttonRemoveatt3.value = "bottom";
  buttonRemoveatt4.value = "Remover do Dashboard";
  buttonRemoveatt5.value = "primary";
  buttonRemoveatt6.value = "removeItemDashboard(this,'"+chartId+"')";
  buttonRemove.setAttributeNode(buttonRemoveatt1);
  buttonRemove.setAttributeNode(buttonRemoveatt2);
  buttonRemove.setAttributeNode(buttonRemoveatt3);
  buttonRemove.setAttributeNode(buttonRemoveatt4);
  buttonRemove.setAttributeNode(buttonRemoveatt5);
  buttonRemove.setAttributeNode(buttonRemoveatt6);

  var spanButtonRemove = document.createElement("span");
  var spanButtonRemoveatt1 = document.createAttribute("class");
  spanButtonRemoveatt1.value = "fa fa-times";
  spanButtonRemove.setAttributeNode(spanButtonRemoveatt1);

  // ------- slider box -------
  // var optionDiv = document.createElement("div");
  // var optionDivatt1 = document.createAttribute("class");
  // var optionDivatt2 = document.createAttribute("style");
  // optionDivatt1.value = "mini-onoffswitch pull-right onoffswitch-primary";
  // optionDivatt2.value = "margin-top:10px;";
  // optionDiv.setAttributeNode(optionDivatt1);
  // optionDiv.setAttributeNode(optionDivatt2);

  // var optionInput = document.createElement("input");
  // var optionInputatt1 = document.createAttribute("type");
  // var optionInputatt2 = document.createAttribute("onclick");
  // var optionInputatt3 = document.createAttribute("name");
  // var optionInputatt4 = document.createAttribute("class");
  // var optionInputatt5 = document.createAttribute("id");
  // var optionInputatt6 = document.createAttribute("checked");
  // optionInputatt1.value = "checkbox";
  // optionInputatt2.value = "addDashboard('"+chartId+"')";
  // optionInputatt3.value = chartId;
  // optionInputatt4.value = "onoffswitch-checkbox";
  // optionInputatt5.value = chartId;
  // optionInput.setAttributeNode(optionInputatt1);
  // optionInput.setAttributeNode(optionInputatt2);
  // optionInput.setAttributeNode(optionInputatt3);
  // optionInput.setAttributeNode(optionInputatt4);
  // optionInput.setAttributeNode(optionInputatt5); 
  // optionInput.setAttributeNode(optionInputatt6);
  
  // var optionLabel = document.createElement("label");
  // var optionLabelatt1 = document.createAttribute("class");
  // var optionLabelatt2 = document.createAttribute("for");
  // optionLabelatt1.value = "onoffswitch-label";
  // optionLabelatt2.value = chartId;
  // optionLabel.setAttributeNode(optionLabelatt1);
  // optionLabel.setAttributeNode(optionLabelatt2);
  // -------------------------

  var panelBody = document.createElement("div");
  var panelBodyatt1 = document.createAttribute("class");
  var panelBodyatt2 = document.createAttribute("style");
  panelBodyatt1.value = "panel-body";
  panelBodyatt2.value = "padding-bottom:50px;";
  panelBody.setAttributeNode(panelBodyatt1);
  panelBody.setAttributeNode(panelBodyatt2);

  var chartNode = document.createElement("div");
  var chartNodeatt1 = document.createAttribute("id");
  chartNodeatt1.value = chartPlotlyId;
  chartNode.setAttributeNode(chartNodeatt1);

  titleNodeBold.appendChild(textTitleNode);
  titleNode.appendChild(titleNodeBold);
  colNode3.appendChild(titleNode);              
  panelHeading.appendChild(colNode3);
  buttonMoveTop.appendChild(spanButtonMoveTop);
  buttonMoveUp.appendChild(spanButtonMoveUp);
  buttonMoveDown.appendChild(spanButtonMoveDown);
  buttonMoveBottom.appendChild(spanButtonMoveBottom);
  buttonSettings.appendChild(spanButtonSettings);
  buttonRemove.appendChild(spanButtonRemove);
  colNode4.appendChild(buttonMoveTop);
  colNode4.appendChild(buttonMoveUp);
  colNode4.appendChild(buttonMoveDown);
  colNode4.appendChild(buttonMoveBottom);
  if(customizable){
    colNode4.appendChild(buttonSettings);
    colNode4.appendChild(buttonRemove);
  }
  // optionDiv.appendChild(optionInput);
  // optionDiv.appendChild(optionLabel);
  // colNode4.appendChild(optionDiv);
  panelHeading.appendChild(colNode4);
  panelBody.appendChild(chartNode);
  panel1.appendChild(panelHeading);
  panel1.appendChild(panelBody);
  colNode2.appendChild(panel1);  
  colNode1.appendChild(colNode2);
  document.getElementById("content").appendChild(colNode1);
}

function buildingConfigureCharts(title,chartPlotlyId,chartId,active) {
  var colNode1 = document.createElement("div");
  var colNode1att1 = document.createAttribute("class");
  var colNode1att2 = document.createAttribute("style");
  colNode1att1.value = "col-md-12";
  colNode1att2.value = "padding:5px;";
  colNode1.setAttributeNode(colNode1att1);
  colNode1.setAttributeNode(colNode1att2);

  var colNode2 = document.createElement("div");
  var colNode2att1 = document.createAttribute("class");
  colNode2att1.value = "col-md-12";
  colNode2.setAttributeNode(colNode2att1);
  
  var panel1 = document.createElement("div");
  var panel1att1 = document.createAttribute("class");
  panel1att1.value = "panel";
  panel1.setAttributeNode(panel1att1);

  var panelHeading = document.createElement("div");
  var panelHeadingatt1 = document.createAttribute("class");
  var panelHeadingatt2 = document.createAttribute("style");
  panelHeadingatt1.value = "panel-heading bg-white border-none";
  panelHeadingatt2.value = "padding:50px;";
  panelHeading.setAttributeNode(panelHeadingatt1);
  panelHeading.setAttributeNode(panelHeadingatt2);
  
  var colNode3 = document.createElement("div");
  var colNode3att1 = document.createAttribute("class");
  colNode3att1.value = "col-md-9 col-sm-9 col-sm-12 text-left";
  colNode3.setAttributeNode(colNode3att1);

  var titleNode = document.createElement("h4");
  var titleNodeBold = document.createElement("b");
  var textTitleNode = document.createTextNode(title);

  var colNode4 = document.createElement("div");
  var colNode4att1 = document.createAttribute("class");
  colNode4att1.value = "col-md-3 col-sm-3 col-sm-12";
  colNode4.setAttributeNode(colNode4att1);              

  var optionDiv = document.createElement("div");
  var optionDivatt1 = document.createAttribute("class");
  var optionDivatt2 = document.createAttribute("style");
  optionDivatt1.value = "mini-onoffswitch pull-right onoffswitch-primary";
  optionDivatt2.value = "margin-top:10px;";
  optionDiv.setAttributeNode(optionDivatt1);
  optionDiv.setAttributeNode(optionDivatt2);              

  var optionInput = document.createElement("input");
  var optionInputatt1 = document.createAttribute("type");
  var optionInputatt2 = document.createAttribute("onclick");
  var optionInputatt3 = document.createAttribute("name");
  var optionInputatt4 = document.createAttribute("class");
  var optionInputatt5 = document.createAttribute("id");
  
  optionInputatt1.value = "checkbox";
  optionInputatt2.value = "addDashboard('"+chartId+"')";
  optionInputatt3.value = chartId;
  optionInputatt4.value = "onoffswitch-checkbox";
  optionInputatt5.value = chartId;
  optionInput.setAttributeNode(optionInputatt1);
  optionInput.setAttributeNode(optionInputatt2);
  optionInput.setAttributeNode(optionInputatt3);
  optionInput.setAttributeNode(optionInputatt4);
  optionInput.setAttributeNode(optionInputatt5);

  if (active) {
    var optionInputatt6 = document.createAttribute("checked");
    optionInput.setAttributeNode(optionInputatt6);
  }
  
  var optionLabel = document.createElement("label");
  var optionLabelatt1 = document.createAttribute("class");
  var optionLabelatt2 = document.createAttribute("for");
  optionLabelatt1.value = "onoffswitch-label";
  optionLabelatt2.value = chartId;
  optionLabel.setAttributeNode(optionLabelatt1);
  optionLabel.setAttributeNode(optionLabelatt2);

  var panelBody = document.createElement("div");
  var panelBodyatt1 = document.createAttribute("class");
  var panelBodyatt2 = document.createAttribute("style");
  panelBodyatt1.value = "panel-body";
  panelBodyatt2.value = "padding-bottom:50px;";
  panelBody.setAttributeNode(panelBodyatt1);
  panelBody.setAttributeNode(panelBodyatt2);

  var chartNode = document.createElement("div");
  var chartNodeatt1 = document.createAttribute("id");
  chartNodeatt1.value = chartPlotlyId;
  chartNode.setAttributeNode(chartNodeatt1);

  titleNodeBold.appendChild(textTitleNode);
  titleNode.appendChild(titleNodeBold);
  colNode3.appendChild(titleNode);              
  panelHeading.appendChild(colNode3);
  optionDiv.appendChild(optionInput);
  optionDiv.appendChild(optionLabel);
  colNode4.appendChild(optionDiv);
  panelHeading.appendChild(colNode4);
  panelBody.appendChild(chartNode);
  panel1.appendChild(panelHeading);
  panel1.appendChild(panelBody);
  colNode2.appendChild(panel1);  
  colNode1.appendChild(colNode2);
  document.getElementById("content").appendChild(colNode1);
}

function buildingEvaluationDashboard(title,chartPlotlyId,chartId) {
  var submit_btn = document.getElementById("submitForm").firstElementChild;

  var colNode1 = document.createElement("div");
  var colNode1att1 = document.createAttribute("class");
  var colNode1att2 = document.createAttribute("style");
  colNode1att1.value = "col-md-12";
  colNode1att2.value = "padding:5px;";
  colNode1.setAttributeNode(colNode1att1);
  colNode1.setAttributeNode(colNode1att2);

  var colNode2 = document.createElement("div");
  var colNode2att1 = document.createAttribute("class");
  colNode2att1.value = "col-md-12";
  colNode2.setAttributeNode(colNode2att1);
  
  var panel1 = document.createElement("div");
  var panel1att1 = document.createAttribute("class");
  panel1att1.value = "panel";
  panel1.setAttributeNode(panel1att1);

  var panelHeading = document.createElement("div");
  var panelHeadingatt1 = document.createAttribute("class");
  var panelHeadingatt2 = document.createAttribute("style");
  panelHeadingatt1.value = "panel-heading bg-white border-none";
  panelHeadingatt2.value = "padding:50px;";
  panelHeading.setAttributeNode(panelHeadingatt1);
  panelHeading.setAttributeNode(panelHeadingatt2);
  
  var colNode3 = document.createElement("div");
  var colNode3att1 = document.createAttribute("class");
  colNode3att1.value = "col-md-12 col-sm-12 col-sm-12 text-left";
  colNode3.setAttributeNode(colNode3att1);

  var titleNode = document.createElement("h4");
  var titleNodeBold = document.createElement("b");
  var textTitleNode = document.createTextNode(title);
  
  var panelBody = document.createElement("div");
  var panelBodyatt1 = document.createAttribute("class");
  var panelBodyatt2 = document.createAttribute("style");
  panelBodyatt1.value = "panel-body";
  panelBodyatt2.value = "padding-bottom:0px;";
  panelBody.setAttributeNode(panelBodyatt1);
  panelBody.setAttributeNode(panelBodyatt2);
  var chartNode = document.createElement("div");
  var chartNodeatt1 = document.createAttribute("id");
  chartNodeatt1.value = chartPlotlyId;
  chartNode.setAttributeNode(chartNodeatt1);

  var divEvaluation = document.createElement("div");
  var divEvaluationatt1 = document.createAttribute("class");
  var divEvaluationatt2 = document.createAttribute("style");
  divEvaluationatt1.value = "col-md-12 bg-white"
  divEvaluationatt2.value = ""
  divEvaluation.setAttributeNode(divEvaluationatt1);
  divEvaluation.setAttributeNode(divEvaluationatt2);

  var divEvaluationInput = document.createElement("div");
  var divEvaluationInputatt1 = document.createAttribute("class");
  var divEvaluationInputatt2 = document.createAttribute("style");
  divEvaluationInputatt1.value = "form-group form-animate-text";
  divEvaluationInputatt2.value = "margin-top:40px !important;"
  divEvaluationInput.setAttributeNode(divEvaluationInputatt1);
  divEvaluationInput.setAttributeNode(divEvaluationInputatt2);
  
  var inputEvaluation = document.createElement("input");
  var inputEvaluationatt1 = document.createAttribute("type");
  var inputEvaluationatt2 = document.createAttribute("class");
  var inputEvaluationatt3 = document.createAttribute("id");
  var inputEvaluationatt4 = document.createAttribute("name");
  var inputEvaluationatt5 = document.createAttribute("required");
  var inputEvaluationatt6 = document.createAttribute("aria-required");
  inputEvaluationatt1.value = "text";
  inputEvaluationatt2.value = "form-text";
  inputEvaluationatt3.value = chartId;
  inputEvaluationatt4.value = chartId;  
  inputEvaluationatt6.value = "true";
  inputEvaluation.setAttributeNode(inputEvaluationatt1);
  inputEvaluation.setAttributeNode(inputEvaluationatt2);
  inputEvaluation.setAttributeNode(inputEvaluationatt3);
  inputEvaluation.setAttributeNode(inputEvaluationatt4);
  inputEvaluation.setAttributeNode(inputEvaluationatt5);
  inputEvaluation.setAttributeNode(inputEvaluationatt6);

  var spanEvaluation = document.createElement("span");
  var spanEvaluationatt1 = document.createAttribute("class");
  spanEvaluationatt1.value = "bar";
  spanEvaluation.setAttributeNode(spanEvaluationatt1);

  var divImportance = document.createElement("div");
  var divImportanceatt1 = document.createAttribute("class");
  var divImportanceatt2 = document.createAttribute("id");
  var divImportanceatt3 = document.createAttribute("style");
  // divImportanceatt1.value = "col-md-12 bg-light2-grey";
  divImportanceatt1.value = "col-md-12 bg-white";
  divImportanceatt2.value = chartId+"#"+"Radio";
  divImportanceatt3.value = 'color: #0a6ebd;';
  divImportance.setAttributeNode(divImportanceatt1);
  divImportance.setAttributeNode(divImportanceatt2);
  divImportance.setAttributeNode(divImportanceatt3);

  var divImportanceSubTopic = document.createElement("div");
  var divImportanceSubTopicatt1 = document.createAttribute("class");
  var divImportanceSubTopicatt2 = document.createAttribute("style");
  divImportanceSubTopicatt1.value = "col-md-3 form-group form-animate-text";
  divImportanceSubTopicatt2.value = "margin-top:20px !important; font-size: 18px;margin-bottom: 15px;";
  divImportanceSubTopic.setAttributeNode(divImportanceSubTopicatt1);
  divImportanceSubTopic.setAttributeNode(divImportanceSubTopicatt2);

  var textEvaluationImportance = document.createTextNode("O quão importante é esse gráfico:");
  divImportanceSubTopic.appendChild(textEvaluationImportance);

  lst_radio_opt = ["Irrelevante","","","Neutro","","","Essencial"];
  lst_option = []
  for(z=0; z<lst_radio_opt.length; z++){
    var divOption = document.createElement("div");
    var divOptionatt1 = document.createAttribute("class");
    var divOptionatt2 = document.createAttribute("style");
    divOptionatt1.value = "col-md-1 form-animate-radio";
    divOptionatt2.value = "margin-top: 20px; display:inline-block; text-align:center;";
    divOption.setAttributeNode(divOptionatt1);
    divOption.setAttributeNode(divOptionatt2);

    var labelRadio = document.createElement("label");
    var labelRadioatt1 = document.createAttribute("class");
    var labelRadioatt2 = document.createAttribute("style");
    labelRadioatt1.value = "radio";
    labelRadioatt2.value = "font-size: 16px; padding: 0px; margin-bottom: 0px;";
    labelRadio.setAttributeNode(labelRadioatt1);
    labelRadio.setAttributeNode(labelRadioatt2);

    var inputRadio = document.createElement("input");
    var inputRadioatt1 = document.createAttribute("type");
    var inputRadioatt2 = document.createAttribute("name");
    var inputRadioatt3 = document.createAttribute("value");
    var inputRadioatt4 = document.createAttribute("id");
    inputRadioatt1.value = "radio";
    inputRadioatt2.value = chartId+"#"+"Radio";
    inputRadioatt3.value = (z+1).toString();
    inputRadioatt4.value = chartId+"#"+"Radio"+"#"+(z+1).toString();
    inputRadio.setAttributeNode(inputRadioatt1);
    inputRadio.setAttributeNode(inputRadioatt2);
    inputRadio.setAttributeNode(inputRadioatt3);
    inputRadio.setAttributeNode(inputRadioatt4);

    var spanRadioOuter = document.createElement("span");
    var spanRadioOuteratt1 = document.createAttribute("class");
    spanRadioOuteratt1.value = "outer";
    spanRadioOuter.setAttributeNode(spanRadioOuteratt1);

    var spanRadioInner = document.createElement("span");
    var spanRadioInneratt1 = document.createAttribute("class");
    spanRadioInneratt1.value = "inner";
    spanRadioInner.setAttributeNode(spanRadioInneratt1);

    var labelRadioText = document.createElement("label");
    var labelRadioTextatt1 = document.createAttribute("style");
    labelRadioTextatt1.value = "font-size: 16px;display:block;";
    labelRadioText.setAttributeNode(labelRadioTextatt1);

    var titleRadio = document.createTextNode(lst_radio_opt[z]);

    spanRadioOuter.appendChild(spanRadioInner);
    labelRadio.appendChild(inputRadio);
    labelRadio.appendChild(spanRadioOuter);
    labelRadioText.appendChild(titleRadio);
    divOption.appendChild(labelRadio);
    divOption.appendChild(labelRadioText);
    lst_option.push(divOption);
  }

  var labelEvaluation = document.createElement("label");
  var textEvaluation = document.createTextNode("Diga dois fatos que você consegue extrair com esse gráfico?");

  titleNodeBold.appendChild(textTitleNode);
  titleNode.appendChild(titleNodeBold);
  colNode3.appendChild(titleNode);
  panelHeading.appendChild(colNode3);  
  panelBody.appendChild(chartNode);
  divImportanceSubTopic.appendChild(textEvaluationImportance);
  divImportance.appendChild(divImportanceSubTopic);
  for(z=0; z<lst_option.length; z++){    
    divImportance.appendChild(lst_option[z]);
  }
  labelEvaluation.appendChild(textEvaluation);
  divEvaluationInput.appendChild(inputEvaluation);
  divEvaluationInput.appendChild(spanEvaluation);
  divEvaluationInput.appendChild(labelEvaluation);
  divEvaluation.appendChild(divEvaluationInput);
  panel1.appendChild(panelHeading);
  panel1.appendChild(panelBody);
  panel1.appendChild(divImportance);
  panel1.appendChild(divEvaluation);
  colNode2.appendChild(panel1);  
  colNode1.appendChild(colNode2);

  document.getElementById("submitForm").insertBefore(colNode1,submit_btn);
}

function buildingModificationDashboard(title,chartPlotlyId,chartId) {
  var submit_btn = document.getElementById("submitForm").firstElementChild;

  var colNode1 = document.createElement("div");
  var colNode1att1 = document.createAttribute("class");
  var colNode1att2 = document.createAttribute("style");
  colNode1att1.value = "col-md-12";
  colNode1att2.value = "padding:5px;";
  colNode1.setAttributeNode(colNode1att1);
  colNode1.setAttributeNode(colNode1att2);

  var colNode2 = document.createElement("div");
  var colNode2att1 = document.createAttribute("class");
  colNode2att1.value = "col-md-12";
  colNode2.setAttributeNode(colNode2att1);
  
  var panel1 = document.createElement("div");
  var panel1att1 = document.createAttribute("class");
  panel1att1.value = "panel";
  panel1.setAttributeNode(panel1att1);

  var panelHeading = document.createElement("div");
  var panelHeadingatt1 = document.createAttribute("class");
  var panelHeadingatt2 = document.createAttribute("style");
  panelHeadingatt1.value = "panel-heading bg-white border-none";
  panelHeadingatt2.value = "padding:50px;";
  panelHeading.setAttributeNode(panelHeadingatt1);
  panelHeading.setAttributeNode(panelHeadingatt2);
  
  var colNode3 = document.createElement("div");
  var colNode3att1 = document.createAttribute("class");
  colNode3att1.value = "col-md-12 col-sm-12 col-sm-12 text-left";
  colNode3.setAttributeNode(colNode3att1);

  var titleNode = document.createElement("h4");
  var titleNodeBold = document.createElement("b");
  var textTitleNode = document.createTextNode(title);
  
  var panelBody = document.createElement("div");
  var panelBodyatt1 = document.createAttribute("class");
  var panelBodyatt2 = document.createAttribute("style");
  panelBodyatt1.value = "panel-body";
  panelBodyatt2.value = "padding-bottom:0px;";
  panelBody.setAttributeNode(panelBodyatt1);
  panelBody.setAttributeNode(panelBodyatt2);
  var chartNode = document.createElement("div");
  var chartNodeatt1 = document.createAttribute("id");
  chartNodeatt1.value = chartPlotlyId;
  chartNode.setAttributeNode(chartNodeatt1);

  var divEvaluation = document.createElement("div");
  var divEvaluationatt1 = document.createAttribute("class");
  var divEvaluationatt2 = document.createAttribute("style");
  divEvaluationatt1.value = "col-md-12 bg-white"
  divEvaluationatt2.value = ""
  divEvaluation.setAttributeNode(divEvaluationatt1);
  divEvaluation.setAttributeNode(divEvaluationatt2);

  var divEvaluationInput = document.createElement("div");
  var divEvaluationInputatt1 = document.createAttribute("class");
  var divEvaluationInputatt2 = document.createAttribute("style");
  divEvaluationInputatt1.value = "form-group form-animate-text";
  divEvaluationInputatt2.value = "margin-top:40px !important;"
  divEvaluationInput.setAttributeNode(divEvaluationInputatt1);
  divEvaluationInput.setAttributeNode(divEvaluationInputatt2);
  
  var inputEvaluation = document.createElement("input");
  var inputEvaluationatt1 = document.createAttribute("type");
  var inputEvaluationatt2 = document.createAttribute("class");
  var inputEvaluationatt3 = document.createAttribute("id");
  var inputEvaluationatt4 = document.createAttribute("name");
  var inputEvaluationatt5 = document.createAttribute("required");
  var inputEvaluationatt6 = document.createAttribute("aria-required");
  inputEvaluationatt1.value = "text";
  inputEvaluationatt2.value = "form-text";
  inputEvaluationatt3.value = chartId;
  inputEvaluationatt4.value = chartId;  
  inputEvaluationatt6.value = "true";
  inputEvaluation.setAttributeNode(inputEvaluationatt1);
  inputEvaluation.setAttributeNode(inputEvaluationatt2);
  inputEvaluation.setAttributeNode(inputEvaluationatt3);
  inputEvaluation.setAttributeNode(inputEvaluationatt4);
  inputEvaluation.setAttributeNode(inputEvaluationatt5);
  inputEvaluation.setAttributeNode(inputEvaluationatt6);

  var spanEvaluation = document.createElement("span");
  var spanEvaluationatt1 = document.createAttribute("class");
  spanEvaluationatt1.value = "bar";
  spanEvaluation.setAttributeNode(spanEvaluationatt1);

  var labelEvaluation = document.createElement("label");
  var textEvaluation = document.createTextNode("Por que você removeu esse gráfico?");

  titleNodeBold.appendChild(textTitleNode);
  titleNode.appendChild(titleNodeBold);
  colNode3.appendChild(titleNode);
  panelHeading.appendChild(colNode3);  
  panelBody.appendChild(chartNode);
  labelEvaluation.appendChild(textEvaluation);
  divEvaluationInput.appendChild(inputEvaluation);
  divEvaluationInput.appendChild(spanEvaluation);
  divEvaluationInput.appendChild(labelEvaluation);
  divEvaluation.appendChild(divEvaluationInput);
  panel1.appendChild(panelHeading);
  panel1.appendChild(panelBody);
  panel1.appendChild(divEvaluation);
  colNode2.appendChild(panel1);  
  colNode1.appendChild(colNode2);

  document.getElementById("submitForm").insertBefore(colNode1,submit_btn);
}

function buildingTamEvaluation(questionList) {
  var submit_btn = document.getElementById("submitForm").firstElementChild;
  lst_radio_opt = ["Discordo","","","Neutro","","","Concordo"];

  var divRoot = document.createElement("div");
  var divRootatt1 = document.createAttribute("class");
  var divRootatt2 = document.createAttribute("style");
  divRootatt1.value = "col-md-12 bg-white border-none";
  divRootatt2.value = "padding:20px;";
  divRoot.setAttributeNode(divRootatt1);
  divRoot.setAttributeNode(divRootatt2);

  var divTAM = document.createElement("div");
  var divTAMatt1 = document.createAttribute("class");
  var divTAMatt2 = document.createAttribute("style");
  divTAMatt1.value = "form-group form-animate-text";
  divTAMatt2.value = "margin-top:20px !important;font-size: 16px;margin-bottom: 15px;";
  divTAM.setAttributeNode(divTAMatt1);
  divTAM.setAttributeNode(divTAMatt2);

  divRoot.appendChild(divTAM);

  for(var key in questionList) {
      var div = document.createElement("div");
      var divatt1 = document.createAttribute("class");
      var divatt2 = document.createAttribute("id");
      divatt1.value = "col-md-12";
      if(key%2==0){
          divatt1.value = "col-md-12 bg-light2-grey";
      }
      divatt2.value = key.toString();
      div.setAttributeNode(divatt1);
      div.setAttributeNode(divatt2);

      var divSubTopic = document.createElement("div");
      var divSubTopicatt1 = document.createAttribute("class");
      var divSubTopicatt2 = document.createAttribute("style");
      divSubTopicatt1.value = "col-md-5 form-group form-animate-text";
      divSubTopicatt2.value = "margin-top:20px !important; font-size: 18px;margin-bottom: 15px;";
      divSubTopic.setAttributeNode(divSubTopicatt1);
      divSubTopic.setAttributeNode(divSubTopicatt2);

      var titleSubTopic = document.createTextNode(questionList[key]); // <-- Question
      divSubTopic.appendChild(titleSubTopic);

      div.appendChild(divSubTopic);
      for(z=0; z<lst_radio_opt.length; z++){
          var divOption = document.createElement("div");
          var divOptionatt1 = document.createAttribute("class");
          var divOptionatt2 = document.createAttribute("style");
          divOptionatt1.value = "col-md-1 form-animate-radio";
          divOptionatt2.value = "margin-top: 20px; display:inline-block; text-align:center;";
          divOption.setAttributeNode(divOptionatt1);
          divOption.setAttributeNode(divOptionatt2);

          var labelRadio = document.createElement("label");
          var labelRadioatt1 = document.createAttribute("class");
          var labelRadioatt2 = document.createAttribute("style");
          labelRadioatt1.value = "radio";
          labelRadioatt2.value = "font-size: 16px; padding: 0px; margin-bottom: 0px;";
          labelRadio.setAttributeNode(labelRadioatt1);
          labelRadio.setAttributeNode(labelRadioatt2);

          var inputRadio = document.createElement("input");
          var inputRadioatt1 = document.createAttribute("type");
          var inputRadioatt2 = document.createAttribute("name");
          var inputRadioatt3 = document.createAttribute("value");
          var inputRadioatt4 = document.createAttribute("id");
          inputRadioatt1.value = "radio";
          inputRadioatt2.value = key.toString(); // <-- Id
          inputRadioatt3.value = (z+1).toString();
          inputRadioatt4.value = key.toString()+"#"+(z+1).toString(); // <-- Id
          inputRadio.setAttributeNode(inputRadioatt1);
          inputRadio.setAttributeNode(inputRadioatt2);
          inputRadio.setAttributeNode(inputRadioatt3);
          inputRadio.setAttributeNode(inputRadioatt4);

          var spanRadioOuter = document.createElement("span");
          var spanRadioOuteratt1 = document.createAttribute("class");
          spanRadioOuteratt1.value = "outer";
          spanRadioOuter.setAttributeNode(spanRadioOuteratt1);

          var spanRadioInner = document.createElement("span");
          var spanRadioInneratt1 = document.createAttribute("class");
          spanRadioInneratt1.value = "inner";
          spanRadioInner.setAttributeNode(spanRadioInneratt1);

          var labelRadioText = document.createElement("label");
          var labelRadioTextatt1 = document.createAttribute("style");
          labelRadioTextatt1.value = "font-size: 16px;display:block;";
          labelRadioText.setAttributeNode(labelRadioTextatt1);
          
          var titleRadio = document.createTextNode(lst_radio_opt[z]);
          
          spanRadioOuter.appendChild(spanRadioInner);
          labelRadio.appendChild(inputRadio);
          labelRadio.appendChild(spanRadioOuter);
          labelRadioText.appendChild(titleRadio);
          divOption.appendChild(labelRadio);
          divOption.appendChild(labelRadioText);
          div.appendChild(divOption);
      }
      divRoot.appendChild(div);

  }
  document.getElementById("submitForm").insertBefore(divRoot,submit_btn);
  
  
}

function loadMenu(menuListInfo,amountSelectedVG) {
  
  // {"id":"materials", 
  // "label_pt":"Materiais acessados", 
  // "label_en":"Materials accessed", 
  // "sub_menu":["estudantes que acessaram", "materiais mais acessados"], 
  // "view":2}
  liList = []
  for (i=0; i<menuListInfo.length; i++){
    curr = menuListInfo[i];

    var liConfigure = document.createElement("li");
    var liConfigureatt1 = document.createAttribute("class");

    if(curr["sub_menu"].length == 0){
      var spanConfigure = document.createElement("span");
      var spanConfigureatt1 = document.createAttribute("class");
      spanConfigureatt1.value = "fa fa-cogs";
      spanConfigure.setAttributeNode(spanConfigureatt1);

      var titleConfigure = document.createTextNode(curr["label_pt"]);
      
      var aConfigure = document.createElement("a");
      var aConfigureatt1 = document.createAttribute("id");
      var aConfigureatt2 = document.createAttribute("href");
      aConfigureatt1.value = "left-menu-"+curr["id"]+"1";
      aConfigureatt2.value = "/eduvis/"+curr["id"]+"1/";
      aConfigure.setAttributeNode(aConfigureatt1);
      aConfigure.setAttributeNode(aConfigureatt2);

      aConfigure.appendChild(spanConfigure);
      aConfigure.appendChild(titleConfigure);

      if( amountSelectedVG[curr["view"]-1] > 0 ){
        var markConfigure = document.createElement("mark");
        var markConfigureatt1 = document.createAttribute("class");
        markConfigureatt1.value = "mark-opt bg-blue";
        markConfigure.setAttributeNode(markConfigureatt1);

        var amountSelected = document.createTextNode(amountSelectedVG[curr["view"]-1].toString());

        var bConfigure = document.createElement("b");
        bConfigure.appendChild(amountSelected);
        markConfigure.appendChild(bConfigure);
        aConfigure.appendChild(markConfigure);
      }
      
      if( window.location.pathname.split("/")[2] == curr["id"]+"1" ){
        liConfigureatt1.value = "active ripple bg-light2-grey hover-opt";
      }else{
        liConfigureatt1.value = "active ripple hover-opt";
      }
      liConfigure.setAttributeNode(liConfigureatt1);
      liConfigure.appendChild(aConfigure);

    } else{
      var ulConfigureSubMenu = document.createElement("ul");
      var ulConfigureSubMenuatt1 = document.createAttribute("class");
      ulConfigureSubMenuatt1.value = "nav nav-list tree";
      ulConfigureSubMenu.setAttributeNode(ulConfigureSubMenuatt1);

      selected = false;
      for(j=0; j<curr["sub_menu"].length; j++){
        curr_submenu = curr["sub_menu"][j];

        if( window.location.pathname.split("/")[2] == curr["id"]+(j+1).toString() ){
          selected = true;
        }

        var aConfigureSubMenu = document.createElement("a");
        var aConfigureSubMenuatt1 = document.createAttribute("id");
        var aConfigureSubMenuatt2 = document.createAttribute("href");
        aConfigureSubMenuatt1.value = "left-menu-"+curr["id"]+(j+1).toString();
        aConfigureSubMenuatt2.value = "/eduvis/"+curr["id"]+(j+1).toString()+"/";
        aConfigureSubMenu.setAttributeNode(aConfigureSubMenuatt1);
        aConfigureSubMenu.setAttributeNode(aConfigureSubMenuatt2);

        var titleConfigureSubMenu = document.createTextNode(curr_submenu);

        var liConfigureSubMenu = document.createElement("li");

        aConfigureSubMenu.appendChild(titleConfigureSubMenu);
        liConfigureSubMenu.appendChild(aConfigureSubMenu);
        ulConfigureSubMenu.appendChild(liConfigureSubMenu);
      }

      var aConfigureMenu = document.createElement("a");
      var aConfigureMenuatt1 = document.createAttribute("class");
      aConfigureMenuatt1.value = "tree-toggle nav-header";
      aConfigureMenu.setAttributeNode(aConfigureMenuatt1);

      var spanConfigure = document.createElement("span");
      var spanConfigureatt1 = document.createAttribute("class");
      spanConfigureatt1.value = "fa fa-cogs";
      spanConfigure.setAttributeNode(spanConfigureatt1);

      var titleConfigure = document.createTextNode(curr["label_pt"]);

      aConfigureMenu.appendChild(spanConfigure);
      aConfigureMenu.appendChild(titleConfigure);

      if( amountSelectedVG[curr["view"]-1] > 0 ){
        var markConfigure = document.createElement("mark");
        var markConfigureatt1 = document.createAttribute("class");
        markConfigureatt1.value = "mark-opt bg-blue";
        markConfigure.setAttributeNode(markConfigureatt1);

        var amountSelected = document.createTextNode(amountSelectedVG[curr["view"]-1].toString());

        var bConfigure = document.createElement("b");
        bConfigure.appendChild(amountSelected);
        markConfigure.appendChild(bConfigure);
        aConfigureMenu.appendChild(markConfigure);
      }

      var spanConfigureArrow = document.createElement("span");
      var spanConfigureArrowatt1 = document.createAttribute("class");
      spanConfigureArrowatt1.value = "fa-angle-right fa right-arrow text-right";
      spanConfigureArrow.setAttributeNode(spanConfigureArrowatt1);

      aConfigureMenu.appendChild(spanConfigureArrow);

      if( selected ){
        liConfigureatt1.value = "active ripple bg-light2-grey hover-opt";
      }else{
        liConfigureatt1.value = "active ripple hover-opt";
      }
      liConfigure.setAttributeNode(liConfigureatt1);
      liConfigure.appendChild(aConfigureMenu);
      liConfigure.appendChild(ulConfigureSubMenu);
      
    }

    liList.push(liConfigure);
    // window.location.pathname.split("/")[2]
  }

  var bDashboard = document.createElement("b");
  var titleDashboard = document.createTextNode("Dashboard");

  var spanDashboard = document.createElement("span");
  var spanDashboardatt1 = document.createAttribute("class");
  spanDashboardatt1.value = "fa fa-bar-chart";
  spanDashboard.setAttributeNode(spanDashboardatt1);

  var aDashboard = document.createElement("a");
  var aDashboardatt1 = document.createAttribute("href");
  aDashboardatt1.value = "/eduvis/customizable_dashboard/";
  aDashboard.setAttributeNode(aDashboardatt1);

  var liDashboard = document.createElement("li");
  var liDashboardatt1 = document.createAttribute("class");
  if( window.location.pathname.split("/")[2] == "customizable_dashboard" ){
    liDashboardatt1.value = "active ripple bg-light2-grey hover-opt";
  }else{
    liDashboardatt1.value = "active ripple hover-opt";
  }  
  liDashboard.setAttributeNode(liDashboardatt1);

  var leftMenuList = document.createElement("ul");
  var leftMenuListatt1 = document.createAttribute("id");
  var leftMenuListatt2 = document.createAttribute("class");
  leftMenuListatt1.value = "left-menu-list";
  leftMenuListatt2.value = "nav nav-list";
  leftMenuList.setAttributeNode(leftMenuListatt1);
  leftMenuList.setAttributeNode(leftMenuListatt2);

  var subLeftMenu = document.createElement("div");
  var subLeftMenuatt1 = document.createAttribute("class");
  subLeftMenuatt1.value = "sub-left-menu scroll";
  subLeftMenu.setAttributeNode(subLeftMenuatt1);

  bDashboard.appendChild(titleDashboard);
  aDashboard.appendChild(spanDashboard);
  aDashboard.appendChild(bDashboard);
  liDashboard.appendChild(aDashboard);
  
  leftMenuList.appendChild(liDashboard);
  for(i=0; i<liList.length; i++){
    leftMenuList.appendChild(liList[i]);
  }  
  
  subLeftMenu.appendChild(leftMenuList);
  document.getElementById("left-menu").appendChild(subLeftMenu);
}

function highlightFieldEmpty(data) {
  Object.entries(data).forEach(([key, value]) => {
    // console.log(key, value);
    el = document.getElementById(key);
    
    var highlight = document.createAttribute("style");
    highlight.value = "color: #e43927;";

    if (el.tagName == "INPUT") {
        if (value == '') {
            var child = el.parentNode.childNodes;
            for (i=0;i<child.length;i++) {
                if (child[i].tagName == 'LABEL'){
                    child[i].setAttributeNode(highlight);
                    break;
                }
            }
        } else {
            var elatt1 = document.createAttribute("value");
            elatt1.value = value;
            el.setAttributeNode(elatt1);
        }
    }

    else if (el.tagName == "SELECT") {
        if (value == '') {
            var parent = el.parentNode;
            var parentatt1 = document.createAttribute("style");
            parentatt1.value = parent.getAttribute('style')+highlight.value;
            parent.setAttributeNode(parentatt1);
        } else {
            var elatt1 = document.createAttribute("selected");
            var child = el.childNodes;            
            for (i=0;i<child.length;i++) {                
                if (child[i].tagName != "OPTION"){
                    continue;
                }
                else if (child[i].getAttribute('value') == value){                        
                    var selected = document.createAttribute("selected");
                    child[i].setAttributeNode(selected);
                    break;
                }
            }
        }
    }

    else if (el.tagName == "DIV") { //likert scale
      console.log(key,"#",value);
      if (value == '') {
        var child = el.firstElementChild;
        var childatt1 = document.createAttribute("style");
        childatt1.value = child.getAttribute('style')+highlight.value;
        child.setAttributeNode(childatt1);
      } else {
        var selected = document.createAttribute("checked");
        document.getElementById(key.toString()+"#"+value).setAttributeNode(selected);
      }
    }
  });

}

function addDashboard(chart_id) {
  function transferComplete(evt) {
    console.log("The transfer is complete.");
  }
  function transferFailed(evt) {
    console.log("An error occurred while transferring the file.");
  }
  function transferCanceled(evt) {
    console.log("The transfer has been canceled by the user.");
  }

  var xhttp = new XMLHttpRequest();
  xhttp.addEventListener("load", transferComplete);
  xhttp.addEventListener("error", transferFailed);
  xhttp.addEventListener("abort", transferCanceled);

  var obj = {"chart": chart_id, "value":document.getElementById(chart_id).checked};
  var obj = JSON.stringify(obj);
  console.log(obj);

  xhttp.open("POST", "/eduvis/add_chart/", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(obj);
}

function moveTopItemDashboard(element,chart_id) {
  console.log("moveTopItemDashboard");

  var elCurr = element.parentNode.parentNode.parentNode.parentNode.parentNode;
  var elRoot = elCurr.parentNode;
  var elPre = elRoot.firstElementChild;

  if (elPre == elCurr){
    return;
  }
  // console.log(obj)

  elRoot.insertBefore(elCurr,elPre);

  function transferComplete(evt) {
    console.log("The transfer is complete.");
  }
  function transferFailed(evt) {
    console.log("An error occurred while transferring the file.");
  }
  function transferCanceled(evt) {
    console.log("The transfer has been canceled by the user.");
  }

  var xhttp = new XMLHttpRequest();
  xhttp.addEventListener("load", transferComplete);
  xhttp.addEventListener("error", transferFailed);
  xhttp.addEventListener("abort", transferCanceled);

  var obj = {"chart": chart_id, "value":"top"};
  var obj = JSON.stringify(obj);
  console.log(obj);

  xhttp.open("POST", "/eduvis/set_order/", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(obj);
}

function moveUpItemDashboard(element,chart_id) {
  console.log("moveUpItemDashboard");
  
  var elCurr = element.parentNode.parentNode.parentNode.parentNode.parentNode;
  var elPre = elCurr.previousElementSibling;
  var elRoot = elCurr.parentNode;

  if (elPre == null){
    return;
  }
  // console.log(obj)

  elRoot.insertBefore(elCurr,elPre);

  function transferComplete(evt) {
    console.log("The transfer is complete.");
  }
  function transferFailed(evt) {
    console.log("An error occurred while transferring the file.");
  }
  function transferCanceled(evt) {
    console.log("The transfer has been canceled by the user.");
  }

  var xhttp = new XMLHttpRequest();
  xhttp.addEventListener("load", transferComplete);
  xhttp.addEventListener("error", transferFailed);
  xhttp.addEventListener("abort", transferCanceled);

  var obj = {"chart": chart_id, "value":"up"};
  var obj = JSON.stringify(obj);
  console.log(obj);

  xhttp.open("POST", "/eduvis/set_order/", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(obj);
}

function moveDownItemDashboard(element,chart_id) {
  console.log("moveDownItemDashboard");
    
  var elCurr = element.parentNode.parentNode.parentNode.parentNode.parentNode;
  var elNext = elCurr.nextElementSibling;
  var elRoot = elCurr.parentNode;

  if (elNext == null){
    return;
  }

  elRoot.insertBefore(elCurr,elNext.nextElementSibling);

  function transferComplete(evt) {
    console.log("The transfer is complete.");
  }
  function transferFailed(evt) {
    console.log("An error occurred while transferring the file.");
  }
  function transferCanceled(evt) {
    console.log("The transfer has been canceled by the user.");
  }

  var xhttp = new XMLHttpRequest();
  xhttp.addEventListener("load", transferComplete);
  xhttp.addEventListener("error", transferFailed);
  xhttp.addEventListener("abort", transferCanceled);

  var obj = {"chart": chart_id, "value":"down"};
  var obj = JSON.stringify(obj);
  console.log(obj);

  xhttp.open("POST", "/eduvis/set_order/", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(obj);
}

function moveBottomItemDashboard(element,chart_id) {
  console.log("moveBottomItemDashboard");

  var elCurr = element.parentNode.parentNode.parentNode.parentNode.parentNode;
  var elRoot = elCurr.parentNode;
  var elNext = elRoot.lastElementChild;

  if (elNext == elCurr){
    return;
  }
  // console.log(obj)

  elRoot.insertBefore(elCurr,elNext.nextElementSibling);

  function transferComplete(evt) {
    console.log("The transfer is complete.");
  }
  function transferFailed(evt) {
    console.log("An error occurred while transferring the file.");
  }
  function transferCanceled(evt) {
    console.log("The transfer has been canceled by the user.");
  }

  var xhttp = new XMLHttpRequest();
  xhttp.addEventListener("load", transferComplete);
  xhttp.addEventListener("error", transferFailed);
  xhttp.addEventListener("abort", transferCanceled);

  var obj = {"chart": chart_id, "value":"bottom"};
  var obj = JSON.stringify(obj);
  console.log(obj);

  xhttp.open("POST", "/eduvis/set_order/", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(obj);
}

function settingsItemDashboard(chart_id) { 
  topic_id = parseInt(chart_id.split("@")[0].replace("T",""));
  console.log(topic_id);
  path = "/eduvis/";
  
  switch (topic_id) {
    case 1:
      path=path.concat("assignments1/");
      console.log("URL: "+path);
      break;
    case 2:
      path=path.concat("assignments2/");
      console.log("URL: "+path);
      break;
    case 3:
      path=path.concat("materials1/");
      console.log("URL: "+path);
      break;
    case 4:
      path=path.concat("materials2/");
      console.log("URL: "+path);
      break;
    case 5:
      path=path.concat("forum1/");
      console.log("URL: "+path);
      break;
    case 6:
      path=path.concat("video_access1/");
      console.log("URL: "+path);
      break;
    case 7:
      path=path.concat("cluster1/");
      console.log("URL: "+path);
      break;
    case 8:
      path=path.concat("cluster3/");
      console.log("URL: "+path);
      break;
    case 9:
      path=path.concat("cluster2/");
      console.log("URL: "+path);
      break;
    case 10:
      path=path.concat("cluster4/");
      console.log("URL: "+path);
      break;
    case 11:
      path=path.concat("cluster5/");
      console.log("URL: "+path);
      break;
    case 12:
      path=path.concat("cluster6/");
      console.log("URL: "+path);
      break;
    case 13:
      path=path.concat("cluster7/");
      console.log("URL: "+path);
      break;
    case 14:
      path=path.concat("age1/");
      console.log("URL: "+path);
      break;
    case 15:
      path=path.concat("age2/");
      console.log("URL: "+path);
      break;
    case 16:
      path=path.concat("age3/");
      console.log("URL: "+path);
      break;
    case 17:
      path=path.concat("age4/");
      console.log("URL: "+path);
      break;
    case 18:
      path=path.concat("prediction1/");
      console.log("URL: "+path);
      break;
    case 19:
      path=path.concat("access1/");
      console.log("URL: "+path);
      break;
    case 20:
      path=path.concat("access2/");
      console.log("URL: "+path);
      break;
    case 21:
      path=path.concat("video_interaction1/");
      console.log("URL: "+path);
      break;
    case 22:
      path=path.concat("video_understood1/");
      console.log("URL: "+path);
      break;
    case 23:
      path=path.concat("navigation1/");
      console.log("URL: "+path);
      break;
    default:
      console.log('Sorry, we are out.');
      return
  }

  window.location.pathname = path;
}

function removeItemDashboard(element,chart_id) {
  console.log("removeItemDashboard");
  console.log(element);
  
  var elCurr = element.parentNode.parentNode.parentNode.parentNode.parentNode
  elCurr.remove();

  function transferComplete(evt) {
    console.log("The transfer is complete.");
  }
  function transferFailed(evt) {
    console.log("An error occurred while transferring the file.");
  }
  function transferCanceled(evt) {
    console.log("The transfer has been canceled by the user.");
  }

  var xhttp = new XMLHttpRequest();
  xhttp.addEventListener("load", transferComplete);
  xhttp.addEventListener("error", transferFailed);
  xhttp.addEventListener("abort", transferCanceled);

  var obj = {"chart": chart_id, "value":false};
  var obj = JSON.stringify(obj);
  console.log(obj);

  xhttp.open("POST", "/eduvis/add_chart/", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send(obj);
}