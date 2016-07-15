// 파일 시스템 모듈
var fs = require('fs');
// 왜 있는지 모르겠음
var url = require('url');
var https = require('https');
// bash 사용
var exec = require('child_process').exec;
// 깃 명령어 및 연동
var simpleGit = require('simple-git')();
// zip 파일 사용
var archiver = require('archiver');
// 깃헙 토큰
var token = '[Your GitHub OAuth Token]';
// 파일 이름
var file_name = './deploy';
// 버전
var version = '122632';
exports.handler = function(event, context) {

    console.log('VERSION: ', version);
    console.log('start to download the ' + file_name + ' via github.');
    // Remote URL 입력
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
