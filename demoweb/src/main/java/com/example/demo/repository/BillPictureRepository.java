package com.example.demo.repository;

import com.example.demo.entity.BillPicture;
import com.example.demo.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface BillPictureRepository extends JpaRepository<BillPicture, String> {
}
