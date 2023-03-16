package com.example.demo.model.bean;

import jakarta.persistence.Column;
import lombok.Data;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

@Data
public class UserBean {
    @NotNull(message = "帳號 - 帳號不可為空")
    @Size(max = 20, message = "帳號 - 輸入字數大於{max}個字")
    private String userId;
    @Size(max = 20, message = "密碼 - 輸入字數大於{max}個字")
    private String password;
    @Size(max = 20, message = "公司 - 輸入字數大於{max}個字")
    private String company;
}
