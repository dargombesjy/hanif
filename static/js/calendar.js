
class Calendar {
    constructor() {
        this.container = document.createElement('div');
        this.year = new Date().getFullYear();
        this.month = new Date().getMonth()
    }
    previous() {
        this.month = this.month - 1;
        if (this.month < 0) {
            this.month = 11;
            this.year = this.year - 1;
        }
        // this.month = this.month == 0 ? 11 : this.month - 1;
        // this.year = this.month == 12 ? this.year - 1 : this.year;
        this.build();
    };
    next() {
        this.month = this.month + 1;
        if (this.month > 11) {
            this.month = 0;
            this.year = this.year + 1;
        }
        this.build();
    };
    monthName = [
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ];
    dayName = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab'];
    getDaysInMonth(year, month) {
        return new Date(year, month + 1, 0).getDate();
    };
    render(year, month) {
        let self = this;
        let days_this_month = this.getDaysInMonth(year, month),
            first_date_this_month = new Date(year, month, 1),
            first_weekday_this_month = first_date_this_month.getDay()

        let prev_month = month == 0 ? 11 : month - 1,
            prev_year = prev_month == 12 ? year - 1 : year,
            prev_month_days = this.getDaysInMonth(prev_year, prev_month);
        
        let weeks = Math.ceil((first_weekday_this_month + days_this_month) / 7);
        let w = 0;  // week day
        let n = 1;  // next day date
        let c = 1;  // current date
        let i = 0;  // count

        let html = `<table class="center">
            <caption>
                <div id="calendar-caption">
                <button id="b-prev">
                    &laquo;
                </button>
                <span><strong>${this.monthName[month]}</strong></span>
                <button id="b-next">
                    &raquo;
                </button>
                </div>
                <div id="calendar-year">${year}</div>
            </caption>
            <thead>
                <tr>
                ${this.dayName.map(item => {
                    return `<td>${item}</td>`
                }).join('')}
                </tr>
            </thead>
            <tbody>
        `;

        for (i = 0; i < weeks * 7; i++) {
            if (w == 0) {
                html += `<tr>`;
            }
            if (i < first_date_this_month.getDay()) {
                html += `<td>${(prev_month_days - first_weekday_this_month + i + 1)}</td>`;
            } else if (c > days_this_month) {
                html += `<td>${n}</td>`;
                n++;
            } else {
                html += `<td>${c}</td>`;
                c++;
            }

            if (w == 7 - 1) {
                html += `</tr>`;
                w = 0;
            } else {
                w++;
            }
        }
        html += `</tbody></table>`;
        // self.element.innerHTML = html;
        self.container.innerHTML = html;
        self.container.querySelector('#b-prev').addEventListener('click', () => {
            this.previous();
        });
        self.container.querySelector('#b-next').addEventListener('click', () => {
            this.next();
        });
        self.container.querySelectorAll('tbody td').forEach((el) => {
            el.addEventListener('click', (e) => {
                this.setValue(e);
            });
        })
        return this.container;

    };
    build() {
        return this.render(this.year, this.month);
    };
    setValue(e) {
        let date = new Date(this.year, this.month, e.target.innerHTML);
        let el = this.container.previousSibling
        el.value = date.toLocaleDateString();
    };
}

