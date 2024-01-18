%亚型拆分，matrix1是第一个亚型的疾病进展序列，10000次MCMC链；matrix2是第二个亚型的疾病进展序列，10000次MCMC链
matrix1 = squeeze(samples_sequence(1,:,:));
matrix2 = squeeze(samples_sequence(2,:,:));

% 创建一个48x48的空矩阵，便于储存数据
% %注意！这里的freq_matrix2是指对第二个亚型进行可视化！如果要对第一个亚型进行可视化，把所有的freq_matrix2改成freq_matrix1
freq_matrix2 = zeros(48,48);

% 遍历每一行，这个循环的目的是综合10000次MCMC链结果，得到最终的亚型疾病进展序列
for i = 1:48
    % 对当前行计算0到47的直方图
    [counts, ~] = histcounts(matrix2(i,:), 0:48);
    % 计算频率并填充到对应的列，注意，10000要改成和MCMC一致
    freq_matrix2(i,:) = counts / 100000;
end

% 1. 把17-32列的数字加入到对应行数的1-16列中，因为第17列和第1列是同一个脑区，以此类推
freq_matrix2(:, 1:16) = freq_matrix2(:, 1:16) + freq_matrix2(:, 17:32);

% 把33到48列的数字也加入到对应行数的1-16列中，同理第33列和第1列是同一个脑区，以此类推。为什么33-48列是脑区的z=3事件，但却不是把33列到48列的数值乘以3呢？这是因为它相比z=2实际上也只累积了z=1。
freq_matrix2(:, 1:16) = freq_matrix2(:, 1:16) + freq_matrix2(:, 33:48);

% 删除17-48列，现在17-48列没用了，因此删除。
freq_matrix2(:, 17:48) = [];

% 2. 创建一个新的48x16的矩阵
new_matrix2 = zeros(42, 16);
for i = 1:16
    for j = 1:48
        new_matrix2(j, i) = sum(freq_matrix2(1:j, i));
    end
end
