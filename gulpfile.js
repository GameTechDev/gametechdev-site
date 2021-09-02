const { series, src, dest } = require('gulp');
const minify = require('gulp-minify');
const concat = require('gulp-concat');

function clean(cb) {

}
function js(cb) {
    src('./assets/js/_src/*.js')
        .pipe(concat('script.js'))
        .pipe(minify({ noSource: true }))
        .pipe(dest('./assets/js/'))
    cb();
}

exports.default = series(js);