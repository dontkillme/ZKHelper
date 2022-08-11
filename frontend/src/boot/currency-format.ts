import { boot } from 'quasar/wrappers';
import currency from 'currency.js';

export default boot(({ app }) => {
	app.config.globalProperties.$window = window;
	app.config.globalProperties.$currency = (value) =>
		currency(value, {
			pattern: '# !',
			negativePattern: '-# !',
			separator: ' ',
			decimal: ',',
			precision: 2,
			symbol: 'zł',
		}).format();
});
