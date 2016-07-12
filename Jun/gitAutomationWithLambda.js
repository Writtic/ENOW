var fs = require('fs');
var url = require('url');
var https = require('https');
var exec = require('child_process').exec;
var simpleGit = require('simple-git')();
var archiver = require('archiver');
var token = '[Your GitHub OAuth Token]';
var file_name = './deploy';
var version = '122632';
exports.handler = function(event, context) {
    console.log('VERSION: ', version);
    console.log('start to download the ' + file_name + ' via github.');
    var remote_url = 'https://' + token + ':x-oauth-basic@github.com/[Your GitHub UserName]/[User GitHub Repo Url]';
    var proc = exec('cd /tmp; rm -rf ./' + file_name, function(error, stdout, stderr) {
        console.log('cleaning the deploy files are completed.');
        var proc = exec('yum -y install git', function(error, stdout, stderr) {
            console.log('complete to install the git.');
            simpleGit
                .clone(remote_url, file_name, function() {
                    console.log('git clone complete from the ' + remote_url);
                    var distzip = fs.createWriteStream(file_name + '.zip');
                    console.log('complete to create the deployment a zip file.');
                    var archive = archiver('zip');
                    distzip.on('close', function() {
                        console.log(file_name + ' compress done. ' + (archive.pointer() / 1024).toFixed(2) + 'KB');
                    });
                    archive.pipe(distzip);
                    console.log('start to compress the zip file.');
                    archive.bulk([{
                        expand: true,
                        cwd: "./" + file_name,
                        src: ["./**/*"],
                        dot: true
                    }]);
                    archive.finalize();
                })
                .outputHandler(function(command, stdout, stderr) {
                    stdout.pipe(process.stdout);
                    stderr.pipe(process.stderr);
                    console.log(stdout);
                    console.log(stderr);
                });
            process.stderr.write(stderr);
            process.stdout.write(stdout);
            console.log(stderr);
            console.log(stdout);
        });
    });
};
