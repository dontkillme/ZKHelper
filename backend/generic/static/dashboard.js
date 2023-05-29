function init() {
  var tabs = {
    infoPoint: new InfoPoint(),
    logisticView: new LogisticView(),
  };
  $('#dashboardsTabs').tabs({
    beforeActivate: (event, ui) => {
      if (tabs[ui.oldPanel.attr('id')]) {
        tabs[ui.oldPanel.attr('id')].hide();
      }
      if (ui.newPanel.attr('id')) {
        tabs[ui.newPanel.attr('id')].show();
      }
    }
  })
}

$(window).on('load', init);

class InfoPoint {
  constructor() {
    this.$view = $("#infoPoint");
    this.init = false;
  }

  show() {
    $.ajax({
        type: 'get',
        url: '/basic/infopoint/',
        context: this
    })
    .fail(onAjaxFail)
    .done(this.onShowSuccess);
  }

  hide() {
  }

  onShowSuccess = (resp) => {
    this.$view.html(resp.view);
    this.data = resp.data;
    this.$view.find("li.participant").on('click', this.getParticipant)
  }

  getParticipant = (e) => {
    let uid = e.target.getAttribute("uid")
    $.ajax({
      type: "get",
      url: `/event/fulleventparticipant/${uid}/`,
      context: this
    })
    .fail(onAjaxFail)
    .done(this.onGetParticipant);
  }

  onGetParticipant = (resp) => {
    if (!resp)
      return
    let $table = this.$view.find("table.basic-info");
    let $fields = $table.find(".field");
    $fields.each((idx, item) => {
      let field = item.getAttribute("name");
      let value = resp[field];
      if (value) {
        $(item).html(value);
      }
    })
  }

}


class LogisticView {
  constructor() {
    this.$view = $("#logisticView");
  }
  show() {
    $.ajax({
        type: 'get',
        url: 'basic/logistic/',
        context: this
    })
    .fail(onAjaxFail)
    .done(this.onShowSuccess);
  }

  hide() {}

  onShowSuccess = (resp) => {
    this.$view.html(resp.view);
    this.data = resp.data;
  }
}


function onAjaxFail(resp) {
  if (resp.responseJSON?.error == '__logout__') {
    window.location.href = "login/";
  }
  if (resp.responseJSON)
    alert(resp.responseJSON.error);
  else
    alert(resp.responseText);
}