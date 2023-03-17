package com.example.demo.model.repository;

import com.example.demo.model.entity.BillPicture;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface BillPictureRepository extends JpaRepository<BillPicture, String> {
}
