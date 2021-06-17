W = [0.6, 0.1, 0.1, 0.1, 0.1;
     0.1, 0.6, 0.1, 0.1, 0.1;
     0.1, 0.1, 0.6, 0.1, 0.1;
     0.1, 0.1, 0.1, 0.6, 0.1;
     0.1, 0.1, 0.1, 0.1, 0.6];%input weights of five nodes (five inputs and five)outputs)
u = [0.6;0.5;0.6;0.2;0.1]; %inputs 
M = [-0.125, 0, 0.125, 0.125, 0;
      0, -0.125, 0, 0.125, 0.125;
      0.125, 0, -0.125, 0, 0.125;
      0.125, 0.125, 0, -0.125, 0;
      0, 0.125, 0.125, 0, -0.125]; %synapse weightings 
[V,D] = eig(M); %eigenvectors are already orthonormal since this is a symmetrical matrix
h = W*u;
diagD = diag(D);
list_A = [];
for i = 1:5
    list_A(:,i) = (dot(h,V(:,i))*V(:,i))./(1-diagD(i));
end
sum(list_A,2)
