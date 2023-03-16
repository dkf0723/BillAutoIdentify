package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.Getter;

@Data
@Entity
@Table(name = "使用者")
public class User {

    @Id
    @Column(name = "帳號",length = 18,nullable= false)
    private String userId;

    @Column(name = "密碼",length = 45,nullable = false)
    private String password;

    @Column(name = "公司",length = 45,nullable = false)
    private String company;

}
