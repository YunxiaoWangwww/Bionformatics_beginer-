mu1 = 5;  
var1 = 0.5^2;
mu2 = 7;
var2 = 1;
yfun = @(mu,var, x)(2*pi*(var))^(-0.5)* exp(-((x-mu).^2)/(2*(var)));
val = fzero(@(x) yfun(mu1, var1, x) - 0.5*yfun(mu2, var2, x), mean([mu1,mu2]))
yval = yfun(mu1, var1, val)
x = [0:0.1:12];
y1 = normpdf(x,mu1,sqrt(var1));
y2 = normpdf(x,mu2,sqrt(var2));
inter_x = fzero(@(x) yfun(mu1, var1, x) - yfun(mu2, var2, x), mean([mu1,mu2]));
inter_y = yfun(mu1, var1, inter_x);
hold on
plot(x,y1,'r', x,y2,'g');
xline(val,'m');
legend('y1','y2','critical threshold');

