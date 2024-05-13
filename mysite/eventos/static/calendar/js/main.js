$(function() {
    const rawData = document.getElementById('events-data').textContent;
    const events = JSON.parse(rawData);
    const validDates = events.map(event => {
      const date = event.start_date.split('T')[0];
      return date;
    });

    rome(inline_cal, { 
      time: false, 
      weekdayFormat: 'short',
      inputFormat: 'YYYY-MM-DD',
      initialValue: validDates[0],
      dateValidator: rome.val.only(validDates)
    });

    const currentDateEl = document.getElementById('current-date');
    const currentDateEventsEl = document.getElementById('current-date-events');
    const nextEventsEl = document.getElementById('next-events');

    function formatDateToPt(date) {
      return new Date(date + 'T03:00:00Z').toLocaleDateString('pt-br');
    }

    function formatDateToISO(date) {
      return new Date(date).toISOString().split('T')[0];
    }

    function createEventElement(event) {
      var eventEl = document.createElement('a');
      eventEl.href = `/eventos/${event.id}/`;
      eventEl.classList.add('list-group-item', 'list-group-item-action');  
      eventEl.innerHTML = `<i class="bi bi-calendar-fill pr-2"></i> ${event.name} ${event.is_eco ? '✅' : '❌'}`
      return eventEl;
    }

    function populateDateEvents(value) {
      currentDateEventsEl.innerHTML = '';
      const validEvents = events.filter(event => {
        return formatDateToISO(value) === formatDateToISO(event.start_date);
      });

      validEvents.forEach(event => {
        var eventEl = createEventElement(event);
        currentDateEventsEl.appendChild(eventEl)
      });
    }

    function populateNextEvents(value) {
      nextEventsEl.innerHTML = '';
      const validEvents = events.filter(event => {
        return formatDateToISO(value) <= formatDateToISO(event.start_date);
      });

      if (validEvents.length == 0){
        nextEventsEl.innerHTML = '<p class="list-group-item">Nenhum evento encontrado</p>'
      }

      validEvents.forEach(event => {
        var eventEl = createEventElement(event);
        nextEventsEl.appendChild(eventEl)
      });
    }

    currentDateEl.innerHTML = formatDateToPt(validDates[0]);
    populateDateEvents(validDates[0]);

    rome(inline_cal).on('data', function (value) {
      currentDateEl.innerHTML = formatDateToPt(value);
      populateDateEvents(value);
    })
    
    const currentDate = new Date().toISOString().split('T')[0];
    populateNextEvents(currentDate)

});