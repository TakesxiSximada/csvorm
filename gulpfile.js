// -*- coding: utf-8 -*-
var fs = require('fs');
var gulp = require('gulp');
var child_process = require('child_process');

gulp.task('test', function (){
    var status = 'stop';
    var cmd = 'nosetests';
    var targets = [
        'src/**/*.py',
        'tests/**/*.py'
    ];

    var testing = (function (event){
        console.log('run: ' +  event.path);
        if(status != 'running'){
            status = 'running';
            var child = child_process.exec(cmd, function (err, stdout, stderr){
                if (!err){
                    console.log('stdout: ' + stdout);
                    console.log('stderr: ' + stderr)
                } else {
                    console.log(err);
                    // err.code will be the exit code of the child process
                    console.log(err.code);
                    // err.signal will be set to the signal that terminated the process
                    console.log(err.signal);
                }
                status = 'stop';
            });
        };
    });

    gulp.watch(targets, function (event){
        testing(event);
    });
});

gulp.task('default', function (){
    gulp.run('test');
});
